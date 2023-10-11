from django.shortcuts import render,redirect
from Customer.models import *
from Owner.models import *
from Manager.models import *
from Admin.models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,'index.html')
def Login(request):
    return render(request,'login.html')
def login_action(request):
    username=request.POST['username']
    password=request.POST['password']
    user=customer_reg_tb.objects.filter(username=username,password=password)
    if(user.count()>0):
        request.session['cid']=user[0].id
        user=auth.authenticate(username=username,password=password)
        auth.login(request,user)
        return redirect('/')
    else:
        user=Owner_reg_tb.objects.filter(username=username,password=password)
        if(user.count()>0):
            if(user[0].status=="Approved"):
                request.session['oid'] = user[0].id
                user=auth.authenticate(username=username,password=password)
                auth.login(request,user)
                return redirect('/')
            elif(user[0].status=="Rejected"):
                messages.add_message(request,messages.INFO,'You are rejected!!!')
                return redirect('Login')
            else:
                messages.add_message(request,messages.INFO,'Verification pending!!!')
                return redirect('Login')
        else:
            user=Admin_tb.objects.filter(username=username,password=password)
            if(user.count()>0):
                request.session['aid'] = user[0].id
                user=auth.authenticate(username=username,password=password)
                auth.login(request,user)
                return redirect('/')
            else:
                user=Manager_tb.objects.filter(username=username,password=password)
                if (user.count() > 0):
                    request.session['mid'] = user[0].id
                    user=auth.authenticate(username=username,password=password)
                    auth.login(request,user)
                    return redirect('/')
                else:
                    user=employee_reg_tb.objects.filter(username=username,password=password)
                    if(user.count()>0):
                        request.session['eid'] = user[0].id
                        user=auth.authenticate(username=username,password=password)
                        auth.login(request,user)
                        return redirect('/')
                    else:
                        messages.add_message(request,messages.INFO,'Incorrect Username/Password')
                        return redirect('Login')
@login_required
def view_owners(request):
    user=Owner_reg_tb.objects.all().exclude(status="Rejected")
    return render(request,'owner_list.html',{'data':user})

@login_required
def Approve(request,oid):
    user=Owner_reg_tb.objects.filter(id=oid).update(status="Approved")
    messages.add_message(request,messages.INFO,'Approved')
    return redirect('view_owners')

@login_required
def Reject(request,oid):
    user=Owner_reg_tb.objects.filter(id=oid).update(status="Rejected")
    messages.add_message(request,messages.INFO,'Rejected')
    return redirect('view_owners')

@login_required
def view_employees_admin(request,oid):
    emplo = employee_reg_tb.objects.filter(owner_id=oid)
    return render(request,'employee_list_admin.html',{'employee':emplo})

def forgot_password(request):
    return render(request,'user_validation.html')

def user_validation_action(request):
    username = request.POST['username']
    customer = customer_reg_tb.objects.filter(username=username)
    owner = Owner_reg_tb.objects.filter(username=username)
    employee = employee_reg_tb.objects.filter(username=username)

    if (customer.count() > 0 or owner.count()>0 or employee.count()>0):
        return render(request, 'user_validation2.html',{'username':username})
    else:
        messages.add_message(request,messages.INFO,'Invalid Username')
        return redirect('forgot_password')

def user_validation2_action(request):
    username = request.POST['username']
    fname = request.POST['fname']
    dob = request.POST['dob']
    mobile = request.POST['mobile']
    customer = customer_reg_tb.objects.filter(username=username,fname=fname,dob=dob,mobile=mobile)
    owner = Owner_reg_tb.objects.filter(username=username,fname=fname,dob=dob,mobile=mobile)
    employee = employee_reg_tb.objects.filter(username=username,fname=fname,dob=dob,mobile=mobile)

    if (customer.count() > 0 or owner.count()>0 or employee.count()>0):
        return render(request, 'forgot_password.html',{'username':username})
    else:
        messages.add_message(request,messages.INFO,'Invalid Details')
        return redirect('forgot_password')
    
def forgot_password_action(request):
    pass1=request.POST['pass1']
    pass2 = request.POST['pass2']
    username = request.POST['username']
    user_auth=User.objects.get(username=username)
    user=customer_reg_tb.objects.filter(username=username)
    if(user.count()>0):
        user.update(password=pass1)
    else:
        user = employee_reg_tb.objects.filter(username=username)
        if (user.count() > 0):
            user.update(password=pass1)
        else:
            user = Owner_reg_tb.objects.filter(username=username)
            if (user.count() > 0):
                user.update(password=pass1)
    user_auth.set_password(pass1)
    user_auth.save()
    messages.add_message(request,messages.INFO,"Password changed!!!")    
    return redirect('Login')

def logout(request):
    if 'cid' in request.session:
        del request.session['cid']
    if 'oid' in request.session:
        del request.session['oid']
    if 'aid' in request.session:
        del request.session['aid']
    if 'mid' in request.session:
        del request.session['mid']
    if 'eid' in request.session:
        del request.session['eid']
    auth.logout(request)
    return redirect('/')

def checkUsername(request):
    username=request.GET['username']
    if 'oid' in request.session and request.GET['emp'] == 'no':
        user1 = Owner_reg_tb.objects.filter(username=username).exclude(id=request.session['oid'])
    else:
        user1 = Owner_reg_tb.objects.filter(username=username)
    if 'eid' in request.session:
        user2 = employee_reg_tb.objects.filter(username=username).exclude(id=request.session['eid'])
    else:
        user2 = employee_reg_tb.objects.filter(username=username)
    if 'cid' in request.session:
        user3 = customer_reg_tb.objects.filter(username=username).exclude(id=request.session['cid'])
    else:
        user3 = customer_reg_tb.objects.filter(username=username)
    
    user4 = Admin_tb.objects.filter(username=username)
    user5 = Manager_tb.objects.filter(username=username)
    if ((user1.count() > 0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        return JsonResponse({'status':'not ok'})
    else:
        return JsonResponse({'status':'ok'})
    




