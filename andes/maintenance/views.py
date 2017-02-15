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
    form = request.POST
    airport_code = (Airport.objects.get(pk=Inventory.objects.filter(machine_number=workorder.machine_number.machine_number).latest('up_date').airport)).code
    return render(request, 'maintenance/confirm_workorder.html', {'workorder': workorder, 'airport_code': airport_code, 'form': form })

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
