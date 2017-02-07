from django.shortcuts import render
from django.http import Http404

from .models import Machine

# Create your views here.
def index(request):
    machine_list = Machine.objects.all()
    context = {'machine_list': machine_list}
    return render(request, 'maintenance/index.html', context)

def pauta(request, machine_number):
    try:
        machine = Machine.objects.get(pk=machine_number)
    except Machine.DoesNotExist:
        raise Http404("Machine does not exist")
    return render(request, 'maintenance/pauta.html', {'machine': machine})
