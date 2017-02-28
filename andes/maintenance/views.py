# -*- coding: utf-8 -*-
import os
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from PyPDF2 import PdfFileMerger, PdfFileReader
from wkhtmltopdf.utils import wkhtmltopdf, render_to_temporary_file
from wkhtmltopdf.views import PDFTemplateResponse

from .models import *

# Create your views here.
def index(request):
    template = 'maintenance/index.html'
    context = {}
    return render(request, template, context)

@login_required
def dashboard(request):
    template = 'maintenance/dashboard.html'
    workorder_list = WorkOrder.objects.all()
    context = {'workorder_list': workorder_list}
    return render(request, template, context)

@login_required
def workorder(request, workorder_number):
    try:
        workorder = WorkOrder.objects.get(pk=workorder_number)
        if workorder.is_closed:
            return HttpResponseForbidden("This WorkOrder is already closed")
    except WorkOrder.DoesNotExist:
        return Http404("This WorkOrder does not exist")

    context = {}
    context['workorder'] = workorder
    context['airport'] = Airport.objects.get(pk=Inventory.objects.filter(machine_number=workorder.machine_number.machine_number).latest('up_date').airport)
    context['inputs'] = Input.objects.all()
    context['spare_parts'] = SparePart.objects.all()
    context['workorder_work_description_list'] = WorkOrderWorkDescription.objects.filter(order_number=workorder.order_number)

    machine_instruction_list = MachineInstruction.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
    context['last_instruction_list'] = machine_instruction_list.filter(instruction_type="Last")
    machine_instruction_list = machine_instruction_list.exclude(instruction_type="Last")

    if workorder.work_type.name == 'Preventivo':
        context['machine_spare_part_list'] = MachineSparePart.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
        context['machine_input_list'] = MachineInput.objects.filter(machine_number=workorder.machine_number, level=workorder.level)

        context['first_instruction_list'] = machine_instruction_list.filter(instruction_type="First")
        machine_instruction_list = machine_instruction_list.exclude(instruction_type="First")
        context['machine_instruction_list'] = machine_instruction_list

        instruction_types = set()
        for i in machine_instruction_list:
            instruction_types.add(i.instruction_type.name)
        context['instruction_types'] = list(instruction_types)

        machine_lubrication_chart_list = MachineLubricationChart.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
        context['machine_lubrication_chart_list'] = machine_lubrication_chart_list
        lubrication_chart_descriptions = []
        for i in machine_lubrication_chart_list:
            for j in LubricationChartDescription.objects.filter(lubrication_chart=i.id):
                lubrication_chart_descriptions.append((j.number, j.description))
        context['lubrication_chart_descriptions'] = sorted(lubrication_chart_descriptions)

        context['today'] = datetime.today()

    template = 'maintenance/workorder.html'

    return render(request, template, context)

@login_required
def process_workorder(request, workorder_number):
    try:
        workorder = WorkOrder.objects.get(pk=workorder_number)
        if workorder.is_closed:
            return HttpResponseForbidden("This WorkOrder is already closed")
    except WorkOrder.DoesNotExist:
        return Http404("This WorkOrder does not exist")

    context = {}
    context['workorder'] = workorder
    context['airport_code'] = (Airport.objects.get(pk=Inventory.objects.filter(machine_number=workorder.machine_number.machine_number).latest('up_date').airport)).code
    context['workorder_work_description_list'] = WorkOrderWorkDescription.objects.filter(order_number=workorder.order_number)
    form = request.POST

    out = map(int, form['output_date'].split("-") + form['output_time'].split(":"))
    out_datetime = datetime(out[0], out[1], out[2], out[3], out[4])
    context['out_datetime'] = out_datetime

    sp_ids = dict((s,form[s]) for s in form.keys() if "spare_part_number" in s and form[s] != "")
    sp_prices = {}
    sp_numbers = {}
    sp_descriptions = {}
    sp_quantitys = dict((s,form[s]) for s in form.keys() if "spare_part_quantity" in s and form[s] != "")
    for key in sp_ids:
        item = SparePart.objects.get(pk=form[key])
        sp_prices[key]=SparePartHistoricPrice.objects.filter(pk=item.id).latest('date').price
        sp_numbers[key]="F:%s S:%s" % (item.factory_number, item.sage_number)
        sp_descriptions[key.replace("number", "description")]=item.spare_part_type

    sp_order_numbers = sorted(sp_numbers)
    sp_order_descriptions = sorted(sp_descriptions)
    sp_order_quantitys = sorted(sp_quantitys)
    sp_order_prices = sorted(sp_prices)

    spare_parts = []
    spare_part_prices = []
    total_costs = []
    if workorder.work_type.name == 'Preventivo':
        machine_spare_part_list = MachineSparePart.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
        for machine_spare_part in machine_spare_part_list:
            msp_number = "F:%s S:%s" % (machine_spare_part.spare_part.factory_number, machine_spare_part.spare_part.sage_number)
            msp_description = machine_spare_part.spare_part.spare_part_type
            msp_quantity = machine_spare_part.quantity
            msp_price = SparePartHistoricPrice.objects.filter(spare_part=machine_spare_part.spare_part.id).latest('date').price
            msp_total_price = msp_price * Decimal(msp_quantity)
            spare_parts.append((msp_number, msp_description, msp_quantity))
            spare_part_prices.append(msp_price)
            total_costs.append(msp_total_price)

    for i in xrange(len(sp_ids)):
        sp_total_price = sp_prices[sp_order_prices[i]] * Decimal(sp_quantitys[sp_order_quantitys[i]])
        spare_parts.append((sp_numbers[sp_order_numbers[i]], sp_descriptions[sp_order_descriptions[i]], sp_quantitys[sp_order_quantitys[i]]))
        spare_part_prices.append(sp_prices[sp_order_prices[i]])
        total_costs.append(sp_total_price)

    is_sp_len_greater_than_0 = len(spare_parts) > 0
    is_sp_even = len(spare_parts)%2 == 1
    if is_sp_even:
        range_sp = [(spare_parts[i], spare_parts[i+1]) for i in xrange(0, len(spare_parts)-1, 2)]
        range_sp.append((spare_parts[len(spare_parts)-1], ("", "", "")))
    else:
        range_sp = [(spare_parts[i], spare_parts[i+1]) for i in xrange(0, len(spare_parts), 2)]

    context['spare_parts'] = {  'range': range_sp,
                                'validator': is_sp_len_greater_than_0,
                            }

    i_ids = dict((s,form[s]) for s in form.keys() if "input_description" in s and form[s] != "")
    i_types = {}
    i_quantitys = dict((s,form[s]) for s in form.keys() if "input_quantity" in s and form[s] != "")
    for key in i_ids:
        i_types[key]= Input.objects.get(pk=form[key]).input_type

    i_order_types = sorted(i_types)
    i_order_quantitys = sorted(i_quantitys)

    inputs = []
    if workorder.work_type.name == 'Preventivo':
        machine_input_list = MachineInput.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
        for machine_input in machine_input_list:
            inputs.append((machine_input.input_number.input_type, machine_input.quantity))

    for i in xrange(len(i_ids)):
        inputs.append((i_types[i_order_types[i]], i_quantitys[i_order_quantitys[i]]))

    is_i_len_greater_than_0 = len(inputs)
    context['inputs'] = {   'range': inputs,
                            'validator': is_i_len_greater_than_0,
                        }

    machine_instruction_list = MachineInstruction.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
    context['last_instruction_list'] = machine_instruction_list.filter(instruction_type="Last")
    machine_instruction_list = machine_instruction_list.exclude(instruction_type="Last")

    if workorder.work_type.name == 'Preventivo':
        context['machine_spare_part_list'] = MachineSparePart.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
        context['machine_input_list'] = MachineInput.objects.filter(machine_number=workorder.machine_number, level=workorder.level)

        context['first_instruction_list'] = machine_instruction_list.filter(instruction_type="First")
        machine_instruction_list = machine_instruction_list.exclude(instruction_type="First")
        context['machine_instruction_list'] = machine_instruction_list

        instruction_types = set()
        for i in machine_instruction_list:
            instruction_types.add(i.instruction_type.name)
        context['instruction_types'] = list(instruction_types)

        machine_lubrication_chart_list = MachineLubricationChart.objects.filter(machine_number=workorder.machine_number, level=workorder.level)
        context['machine_lubrication_chart_list'] = machine_lubrication_chart_list
        lubrication_chart_descriptions = []
        for i in machine_lubrication_chart_list:
            for j in LubricationChartDescription.objects.filter(lubrication_chart=i.id):
                lubrication_chart_descriptions.append((j.number, j.description))
        context['lubrication_chart_descriptions'] = sorted(lubrication_chart_descriptions)

        context['today'] = datetime.today()

    workorder_template = 'maintenance/process_workorder.html'
    header_template = 'maintenance/guideline_header.html'
    footer_template = 'maintenance/guideline_footer.html'
    stylesheet = 'maintenance/stylesheet.css'
    cmd_options = { 'encoding': 'utf8',
                    'quiet': True,
                    'page-size': 'Letter',
                    'user-style-sheet': stylesheet,
                    'print-media-type': True,
                    }

    directory = settings.MEDIA_ROOT + str(workorder.machine_number.machine_number) + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    workorder_temp_file = render_to_temporary_file(template=get_template(workorder_template), context=context, request=request)
    header_temp_file = render_to_temporary_file(template=get_template(header_template), context=context, request=request)
    footer_temp_file = render_to_temporary_file(template=get_template(footer_template), context=context, request=request)

    workorder_filename = directory + "workorder"
    wkhtmltopdf(pages=[workorder_temp_file.name], output=workorder_filename, **cmd_options)
    cmd_options['header-html'] = header_temp_file.name
    cmd_options['footer-html'] = footer_temp_file.name

    if workorder.work_type.name == 'Preventivo':
        guideline_template = 'maintenance/guideline.html'
        guideline_temp_file = render_to_temporary_file(template=get_template(guideline_template), context=context, request=request)
        guideline_filename = directory + "guideline"
        wkhtmltopdf(pages=[guideline_temp_file.name], output=guideline_filename, **cmd_options)
    else:
        exit_checklist_template = 'maintenance/exit_checklist.html'
        exit_checklist_temp_file = render_to_temporary_file(template=get_template(exit_checklist_template), context=context, request=request)
        exit_checklist_filename = directory + "exit_checklist"
        wkhtmltopdf(pages=[exit_checklist_temp_file.name], output=exit_checklist_filename, **cmd_options)

    filename = directory + str(out_datetime)
    merger = PdfFileMerger()
    merger.append(PdfFileReader(file(workorder_filename, 'rb')))
    if workorder.work_type.name == 'Preventivo':
        merger.append(PdfFileReader(file(guideline_filename, 'rb')))
    else:
        merger.append(PdfFileReader(file(exit_checklist_filename, 'rb')))
    merger.write(filename)

    os.remove(workorder_filename)
    if workorder.work_type.name == 'Preventivo':
        os.remove(guideline_filename)
    else:
        os.remove(exit_checklist_filename)

    filename = str(workorder.machine_number.machine_number) + "/" + str(out_datetime)
    workorder.out_datetime = out_datetime
    workorder.mechanic = User.objects.get(pk=request.user.id)
    workorder.annex = filename
    workorder.is_closed = True
    workorder.save()

    cmd_options['header-html'] = None
    cmd_options['footer-html'] = None

    context['spare_parts'] = {  'list': spare_parts,
                                'validator': is_sp_len_greater_than_0,
                                }
    context['total_costs'] = total_costs
    subdirectory = directory + "purchase_order/"
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    purchase_order_template = 'maintenance/purchase_order.html'
    purchase_order_temp_file = render_to_temporary_file(template=get_template(purchase_order_template), context=context, request=request)
    purchase_order_filename = subdirectory + str(out_datetime)
    short_purchase_order_filename = str(workorder.machine_number.machine_number) + "/purchase_order/" + str(out_datetime)
    wkhtmltopdf(pages=[purchase_order_temp_file.name], output=purchase_order_filename, **cmd_options)
    purchase_order = PurchaseOrder(work_order=workorder, estimate = short_purchase_order_filename)
    purchase_order.save()

    download_template = 'maintenance/download.html'
    download_context = {'pdf_url': str(workorder.machine_number.machine_number) + "/" + str(out_datetime)}
    return render (request, download_template, download_context)

@login_required
def get_work_description(request, suffix):
    new_suffix = str(int(suffix) + 1)
    template = 'maintenance/work_description.html'
    context = {'suffix': new_suffix}
    return render(request, template, context)

@login_required
def get_spare_part_list(request, suffix):
    spare_part_list = SparePart.objects.all()
    new_suffix = str(int(suffix) + 1)
    template = 'maintenance/spare_part_list.html'
    context = {'spare_part_list': spare_part_list, 'suffix': new_suffix}
    return render(request, template, context)

@login_required
def get_spare_part_type(request, id):
    try:
        spare_part_type = SparePart.objects.get(pk=id).spare_part_type
    except SparePart.DoesNotExist:
        return Http404("SparePart does not exist")
    return HttpResponse(spare_part_type)

@login_required
def get_input_list(request, suffix):
    input_list = Input.objects.all()
    new_suffix = str(int(suffix) + 1)
    template = 'maintenance/input_list.html'
    context = {'input_list': input_list, 'suffix': new_suffix}
    return render(request, template, context)
