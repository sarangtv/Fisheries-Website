from django.shortcuts import render,redirect
from Customer.models import *
from Owner.models import *
from Manager.models import *
from Admin.models import *
from Employee.models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def view_alerts(request):
    alerts = Alert_tb.objects.filter(status='pending').order_by('-id')
    return render(request,'alert.html',{'alert':alerts})

@login_required
def alertEmployeeDetails(request,eid):
    emp=employee_reg_tb.objects.get(id=eid)
    return render(request,'emp_details.html',{'data':emp})

@login_required
def readAlert(request,aid):
    alert=Alert_tb.objects.filter(id=aid).update(status='read')
    return redirect('view_alerts')

@login_required
def view_auctions_manager(request):
    details=fisher_fish.objects.all().order_by('-id')
    return render(request,'view_auctions_manager.html',{'dtls':details})

@login_required
def view_details_manager(request,v_id):
    fish=fisher_fish.objects.get(id=v_id)
    return render(request,'view_details_manager.html',{'fs':fish})

@login_required
def view_complaints(request):
    complaints=complaint_tb.objects.all().order_by('-id')
    return render(request,'view_complaints_manager.html',{'cmp':complaints})

@login_required
def complaint_detail(request,comp_id):
    complaint=complaint_tb.objects.get(id=comp_id)
    return render(request,'complaint_detail.html',{'cmp':complaint})

@login_required
def reply_action(request):
    comp_id=request.POST['hid']
    cmp=complaint_tb.objects.get(id=comp_id)
    subject=request.POST['subject']
    reply=request.POST['reply']
    date = datetime.date.today()
    time = datetime.datetime.now().strftime("%H:%M")
    reply=reply_tb(compl_id=cmp,subject=subject,reply=reply,date=date,time=time)
    reply.save()
    complaint=complaint_tb.objects.filter(id=comp_id).update(status='replied')
    messages.add_message(request,messages.INFO,"Reply added!!!")
    return redirect('complaint_detail',comp_id=comp_id)
