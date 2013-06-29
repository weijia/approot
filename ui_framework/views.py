# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse
from django.shortcuts import render_to_response

#from django.conf import settings
import os

def index(request):
    return render_to_response('ui_framework/index.html')
    #return render_to_response('class_scheduling/class_scheduling.html', {'columns':[[{"title":"Pending to schedule", "id":"class_need_to_schedule_panel"}]]})
