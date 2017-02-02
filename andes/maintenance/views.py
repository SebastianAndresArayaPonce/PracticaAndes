from django.shortcuts import render
from django.http import HttpResponse
from .models import Airport

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the maintenance index.")

def air(request):
    airport_list = Airport.objects.all()
    context = { 'airport_list': airport_list, }
    return render(request, 'maintenance/index.html', context)
