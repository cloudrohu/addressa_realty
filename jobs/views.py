from django.shortcuts import render
from .models import *
from home.models import Setting

app_name = "jobs"

def career(request):
    settings_obj = Setting.objects.filter(status="True").first()    
    
    context = {
        "settings_obj": settings_obj,

    }
    return render(request, 'jobs/career.html', context)