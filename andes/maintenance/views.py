from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404, HttpResponse

from .models import Machine, SparePart, MachineSparePart, Input, MachineInput, MachineInstruction, WorkOrder, Inventory, Airport

# Create your views here.
def index(request):
    machine_list = Machine.objects.all()
    context = {'machine_list': machine_list}
    return render(request, 'maintenance/index.html', context)

@login_required
def guideline(request, machine_number, level):
    try:
        machine = Machine.objects.get(pk=machine_number)
    except Machine.DoesNotExist:
        raise Http404("Machine does not exist")
    machine_spare_part_list = MachineSparePart.objects.filter(machine_number=machine_number, level=level)
    machine_input_list = MachineInput.objects.filter(machine_number=machine_number, level=level)
    machine_instruction_list = MachineInstruction.objects.filter(machine_number=machine_number, level=level)
    context = {'machine': machine, 'machine_spare_part_list': machine_spare_part_list, 'machine_input_list': machine_input_list, 'machine_instruction_list': machine_instruction_list}
    return render(request, 'maintenance/guideline.html', context)

@login_required
def workorder(request, workorder_number):
    try:
        workorder = WorkOrder.objects.get(pk=workorder_number)
    except WorkOrder.DoesNotExist:
        raise Http404("WorkOrder does not exist")
    airport = Airport.objects.get(pk=Inventory.objects.filter(machine_number=workorder.machine_number.machine_number).latest('up_date').airport)
    inputs = Input.objects.all()
    spare_parts = SparePart.objects.all()
    return render(request, 'maintenance/workorder.html', {'workorder': workorder, 'airport': airport, 'inputs': inputs, 'spare_parts': spare_parts})

@login_required
def confirm_workorder(request, workorder_number):
    try:
        workorder = WorkOrder.objects.get(pk=workorder_number)
    except WorkOrder.DoesNotExist:
        raise Http404("WorkOrder does not exist")
    airport_code = (Airport.objects.get(pk=Inventory.objects.filter(machine_number=workorder.machine_number.machine_number).latest('up_date').airport)).code
    form = request.POST

    w_entries = dict((s,form[s]) for s in form.keys() if "work_description" in s)
    w_order = sorted(w_entries)
    is_w_len_greater_than_0 = len(w_entries) > 0
    work_descriptions = {'entries': w_entries, 'order': w_order, 'validator': is_w_len_greater_than_0}

    sp_all = SparePart.objects.all()
    sp_numbers = dict((s,form[s]) for s in form.keys() if "spare_part_number" in s)
    sp_quantitys = dict((s,form[s]) for s in form.keys() if "spare_part_quantity" in s)
    sp_order = sorted(sp_numbers)
    is_sp_len_greater_than_0 = len(sp_numbers) > 0
    is_sp_even = len(sp_numbers)%2 == 1
    range_sp = [(sp_order[i], sp_order[i+1]) for i in xrange(0, len(sp_numbers)/2+1, 2)]
    if is_sp_even:
        range_sp.append((sp_order[len(sp_numbers)], ""))
    spare_parts = {'all': sp_all, 'numbers': sp_numbers, 'quantitys': sp_quantitys, 'range': range_sp, 'validator': is_sp_len_greater_than_0}

    i_entries = dict((s,form[s]) for s in form.keys() if "input_description" in s)
    i_quantitys = dict((s,form[s]) for s in form.keys() if "input_quantity" in s)
    is_i_len_greater_than_0 = len(i_entries)
    i_order = sorted(i_entries)
    input_descriptions = {'entries': i_entries, 'quantitys': i_quantitys, 'order': i_order, 'validator': is_i_len_greater_than_0}

    context = {'workorder': workorder, 'airport_code': airport_code, 'work_descriptions': work_descriptions, 'spare_parts': spare_parts, 'input_descriptions': input_descriptions, 'form': form }
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    #print form
    for key in work_descriptions['order']:
        print key
    #print spare_parts['numbers'][x]
    #print range_sp
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    #print sp_numbers
    return render(request, 'maintenance/confirm_workorder.html', context)

@login_required
def process_workorder(request):
    return render(request, 'maintenance/index.html', {})

@login_required
def get_work_description(request, suffix):
    new_suffix = str(int(suffix) + 1)
    return render(request, 'maintenance/work_description.html', {'suffix': new_suffix})

@login_required
def get_spare_part_list(request, suffix):
    spare_part_list = SparePart.objects.all()
    new_suffix = str(int(suffix) + 1)
    return render(request, 'maintenance/spare_part_list.html', {'spare_part_list': spare_part_list, 'suffix': new_suffix})

@login_required
def get_spare_part_type(request, id):
    try:
        spare_part_type = SparePart.objects.get(pk=id).spare_part_type
    except SparePart.DoesNotExist:
        raise Http404("SparePart does not exist")
    return HttpResponse(spare_part_type)

@login_required
def get_input_list(request, suffix):
    input_list = Input.objects.all()
    new_suffix = str(int(suffix) + 1)
    return render(request, 'maintenance/input_list.html', {'input_list': input_list, 'suffix': new_suffix})
