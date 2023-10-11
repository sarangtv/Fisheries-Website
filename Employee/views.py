from django.shortcuts import render
from Owner.models import *
from Employee.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import datetime
import time
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def alert_manager(request):
    emp=employee_reg_tb.objects.get(id=request.session['eid'])
    date=datetime.date.today()
    alert = Alert_tb(empl_id=emp, date=date, time=datetime.datetime.now().strftime("%H:%M"))
    alert.save()
    try:
        send_mail("Emergency",emp.boat_id.name+" under "+emp.owner_id.username+" in danger!!",settings.EMAIL_HOST_USER,['fathimthus@gmail.com'])
        msg="Alert send successfully!!!"
        
    except Exception as e:
        msg="Alert Sending sucsessfully!" 
    return JsonResponse({'msg':msg})
