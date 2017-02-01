from django.shortcuts import render
from django.http import HttpResponse

from .models import Airport

# Create your views here.
def index(request):
    airport_list = Airport.objects.all()
    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    #print airport_list
    #output = ', '.join([q.name for q in airport_list])
    #return HttpResponse(output)
    context = { 'airport_list': airport_list, }
    return render(request, 'maintenance/index.html', context)
