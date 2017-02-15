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

    w_entries = dict((s,form[s]) for s in form.keys() if "work_description" in s and form[s] != "")
    w_order = sorted(w_entries)
    is_w_len_greater_than_0 = len(w_entries) > 0
    work_descriptions = {'entries': w_entries, 'order': w_order, 'validator': is_w_len_greater_than_0}

    sp_ids = dict((s,form[s]) for s in form.keys() if "spare_part_number" in s and form[s] != "")
    sp_numbers = {}
    sp_descriptions = {}
    sp_quantitys = dict((s,form[s]) for s in form.keys() if "spare_part_quantity" in s and form[s] != "")
    for key in sp_ids:
        item = SparePart.objects.get(pk=form[key])
        sp_numbers[key]="F:%s S:%s" % (item.factory_number, item.sage_number)
        sp_descriptions[key]=item.spare_part_type
    sp_order_numbers = sorted(sp_numbers)
    sp_order_quantitys = sorted(sp_quantitys)
    sp_order_descriptions = sorted(sp_descriptions)
    is_sp_len_greater_than_0 = len(sp_ids) > 0
    is_sp_even = len(sp_ids)%2 == 1
    if is_sp_even:
        range_sp = [(sp_order_numbers[i], sp_order_descriptions[i], sp_order_quantitys[i], sp_order_numbers[i+1], sp_order_descriptions[i+1], sp_order_quantitys[i+1]) for i in xrange(0, len(sp_ids)-1, 2)]
        range_sp.append((sp_order_numbers[len(sp_ids)-1], sp_order_descriptions[len(sp_ids)-1], sp_order_quantitys[len(sp_ids)-1], "", "", ""))
    else:
        range_sp = [(sp_order_numbers[i], sp_order_quantitys[i], sp_order_descriptions[i], sp_order_numbers[i+1], sp_order_quantitys[i+1], sp_order_descriptions[i+1]) for i in xrange(0, len(sp_ids), 2)]
    spare_parts = {'numbers': sp_numbers, 'descriptions': sp_descriptions, 'quantitys': sp_quantitys, 'range': range_sp, 'validator': is_sp_len_greater_than_0}

    i_ids = dict((s,form[s]) for s in form.keys() if "input_description" in s and form[s] != "")
    i_types = {}
    #i_descriptions = {}
    i_quantitys = dict((s,form[s]) for s in form.keys() if "input_quantity" in s and form[s] != "")
    for key in i_ids:
        item = Input.objects.get(pk=form[key])
        i_types[key]= item.input_type
        #i_descriptions[key]=item.description
    i_order_types = sorted(i_types)
    #i_order_descriptions = sorted(i_descriptions)
    i_order_quantitys = sorted(i_quantitys)
    is_i_len_greater_than_0 = len(i_ids)
    #range_i = [(i_order_types[i], i_order_descriptions[i], i_order_quantitys[i]) for i in xrange(len(i_ids))]
    range_i = [(i_order_types[i],i_order_quantitys[i]) for i in xrange(len(i_ids))]
    #inputs = {'types': i_types, 'descriptions': i_descriptions, 'quantitys': i_quantitys, 'range': range_i, 'validator': is_i_len_greater_than_0}
    inputs = {'types': i_types, 'quantitys': i_quantitys, 'range': range_i, 'validator': is_i_len_greater_than_0}

    context = {'workorder': workorder, 'airport_code': airport_code, 'work_descriptions': work_descriptions, 'spare_parts': spare_parts, 'inputs': inputs}
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
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
