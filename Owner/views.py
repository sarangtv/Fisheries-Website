from django.shortcuts import render,redirect
from Owner.models import *
from Customer.models import *
from Admin.models import *
from Manager.models import *
import datetime
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
def Owner_registration(request):
    return render(request, 'owner_reg.html')

def Owner_reg_action(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    address = request.POST['address']
    dob = request.POST['dob']
    mobile = request.POST['mobile']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    myproof = ''
    if(len(request.FILES)>0):
        myproof=request.FILES['file']
    else:
        myproof="No proof"
    user = Owner_reg_tb.objects.filter(username=username)
    user2 = customer_reg_tb.objects.filter(username=username)
    user3 = Admin_tb.objects.filter(username=username)
    user4 = Manager_tb.objects.filter(username=username)
    user5 = employee_reg_tb.objects.filter(username=username)
    if ((user.count() > 0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        messages.add_message(request,messages.INFO,"Username already exist!!!")
    else:
        user = Owner_reg_tb(fname=fname, lname=lname, address=address, dob=dob, mobile=mobile,email=email, username=username,
                               password=password,status='pending',proof=myproof)
        user.save()
        user=User.objects.create_user(username=username,password=password)
        user.save()
        messages.add_message(request,messages.INFO,"Registration successful")
    return redirect('Owner_registration')

@login_required    
def add_boat(request):
    return render(request,'boat_reg.html')

@login_required
def add_boat_action(request):
    name = request.POST['name']
    regno = request.POST['regno']
    owner_id = request.session['oid']
    owner=Owner_reg_tb.objects.get(id=owner_id)
    no_of_empl = request.POST['no_of_empl']
    bt = ''
    if (len(request.FILES) > 0):
        bt = request.FILES['photo']
    else:
        bt = "No photo"
    boat = fisher_boat(name=name, regno=regno, photo=bt, owner_id=owner, no_of_empl=no_of_empl)
    boat.save()
    messages.add_message(request,messages.INFO,"Added boat successfully")
    return redirect('add_boat')

@login_required
def add_employee(request):
    boats=fisher_boat.objects.filter(owner_id=request.session['oid'])
    return render(request,'add_employee.html',{'boats':boats})

@login_required
def add_employee_action(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    address = request.POST['address']
    dob = request.POST['dob']
    email = request.POST['email']
    mobile = request.POST['mobile']
    boat_id = request.POST['boats']
    username = request.POST['username']
    password = request.POST['password']
    owner_obj = Owner_reg_tb.objects.get(id=request.session['oid'])
    boat=fisher_boat.objects.get(id=boat_id)
    user = Owner_reg_tb.objects.filter(username=username)
    user2 = customer_reg_tb.objects.filter(username=username)
    user3 = Admin_tb.objects.filter(username=username)
    user4 = Manager_tb.objects.filter(username=username)
    user5 = employee_reg_tb.objects.filter(username=username)
    if((user.count() > 0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        messages.add_message(request,messages.INFO,"Username already exist!!!")
    else:
        empl=employee_reg_tb.objects.filter(boat_id=boat_id)
        if(empl.count()<boat.no_of_empl):
            employee = employee_reg_tb(fname=fname,lname=lname,owner_id=owner_obj,address=address,dob=dob,email=email,mobile=mobile,boat_id=boat,username=username,password=password)
            employee.save()
            user=User.objects.create_user(username=username,password=password)
            user.save()
            messages.add_message(request,messages.INFO,"Added employee successfully")
        else:
            messages.add_message(request,messages.INFO,"Employee count exceeds!!!")
    return redirect('add_employee')

@login_required
def view_boats(request):
    boats = fisher_boat.objects.filter(owner_id=request.session['oid'])
    return render(request, 'boat_list.html',{'boat':boats})

@login_required
def Update_boat(request,bid):
    boat=fisher_boat.objects.filter(id=bid)
    return render(request,'update_boat.html',{'data':boat})

@login_required
def Update_boat_action(request):
    name=request.POST['name']
    regno=request.POST['regno']
    no_of_empl=request.POST['no_of_empl']
    boat_id=request.POST['hid']
    boat=fisher_boat.objects.get(id=boat_id)
    bt = ''
    if (len(request.FILES) > 0):
        bt = request.FILES['photo']
    else:
        bt = boat.photo
    boat.name=name
    boat.regno=regno
    boat.no_of_empl=no_of_empl
    boat.photo=bt
    boat.save()
    messages.add_message(request,messages.INFO,"Updated successfully!!!")
    return redirect('Update_boat',bid=boat_id)

@login_required
def Delete_boat(request,bid):
    boat=fisher_boat.objects.filter(id=bid).delete()
    messages.add_message(request,messages.INFO,"Deleted successfully!!!")
    return redirect('view_boats')

@login_required
def view_employees(request):
    emp = employee_reg_tb.objects.filter(owner_id=request.session['oid'])
    return render(request, 'employee_list.html',{'employee':emp})

@login_required
def Delete_employee(request,eid):
    employee = employee_reg_tb.objects.filter(id=eid).delete()
    messages.add_message(request,messages.INFO,"Deleted successfully!!!")
    return redirect('view_employees')

@login_required
def add_fish(request):
    return render(request,'add_fish.html')

@login_required
def add_fish_action(request):
    name = request.POST['name']
    quantity = request.POST['quantity']
    price = request.POST['price']
    start_time=request.POST['start_time']
    print(start_time)
    end_time=request.POST['end_time']
    owner_id = request.session['oid']
    owner = Owner_reg_tb.objects.get(id=owner_id)
    fs = ''
    if (len(request.FILES) > 0):
        fs = request.FILES['photo']
    else:
        fs = "No photo"
    fish = fisher_fish(name=name, photo=fs,quantity=quantity,price=price,start_time=start_time,end_time=end_time,date=datetime.datetime.date(datetime.datetime.now()), owner_id=owner)

    fish.save()
    messages.add_message(request,messages.INFO,"Added fish successfully")
    return redirect('add_fish')

@login_required
def view_fish(request):
    owner_id = request.session['oid']
    fish=fisher_fish.objects.filter(owner_id=owner_id).order_by('-id')
    return render(request, 'list_fish.html', {'fish': fish})

@login_required
def delete_fish(request,fid):
     fish = fisher_fish.objects.filter(id=fid)
     fishname=fish[0].name
     fish.delete()
     messages.add_message(request,messages.INFO,"Deleted "+fishname)
     return redirect('view_fish')

@login_required    
def update_fish(request,fid):
     fish=fisher_fish.objects.filter(id=fid)
     return render(request, 'update_fish.html', {'fish': fish})

@login_required    
def update_fish_action(request):
    name=request.POST['name']
    quantity=request.POST['quantity']
    price=request.POST['price']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    fish_id = request.POST['hid']
    f = fisher_fish.objects.get(id=fish_id)
    fs = ''
    if (len(request.FILES) > 0):
        fs = request.FILES['photo']
    else:
        fs = f.photo

    f.name=name
    f.quantity=quantity
    f.price=price
    f.start_time=start_time
    f.end_time=end_time
    f.photo=fs
    f.save()
    messages.add_message(request,messages.INFO,"updated successfully")
    return redirect('update_fish',fid=fish_id)

@login_required
def fish_view_auction(request,fish_id):
    auctn=bidding.objects.filter(fish_id=fish_id).order_by('-price')
    return render(request,'fish_view_auction.html',{'auctn':auctn,'fish_id':fish_id})

@login_required
def cust_details(request,cust_id,fish_id):
    cust=customer_reg_tb.objects.filter(id=cust_id)
    return render(request,'cust_details.html',{'customer':cust,'fish_id':fish_id})

@login_required
def view_profile_owner(request):
    ownr=Owner_reg_tb.objects.filter(id=request.session['oid'])
    return render(request, 'owner_profile.html', {'owner': ownr})

@login_required
def update_owner_profile(request):
    fname=request.POST['fname']
    lname=request.POST['lname']
    address=request.POST['address']
    dob=request.POST['dob']
    mobile=request.POST['mobile']
    email = request.POST['email']
    username=request.POST['username']
    password=request.POST['password']
    myproof = ''
    ownr = Owner_reg_tb.objects.get(id=request.session['oid'])
    auth_owner=User.objects.get(username=ownr.username)
    if (len(request.FILES) > 0):
        myproof = request.FILES['file']
    else:
        myproof = ownr.proof
    user = Owner_reg_tb.objects.filter(username=username).exclude(id=request.session['oid'])
    user2 = customer_reg_tb.objects.filter(username=username)
    user3 = Admin_tb.objects.filter(username=username)
    user4 = Manager_tb.objects.filter(username=username)
    user5 = employee_reg_tb.objects.filter(username=username)
    if ((user.count() > 0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        messages.add_message(request,messages.INFO,"Username already exist!!!")
    else:
        ownr.fname=fname
        ownr.lname=lname
        ownr.address=address
        ownr.dob=dob
        ownr.mobile=mobile
        ownr.email=email
        ownr.usernme=username
        ownr.password=password
        ownr.proof=myproof
        ownr.save()
        auth_owner.username=username
        auth_owner.set_password(password)
        auth_owner.save()
        auth.authenticate(username=username,password=password)
        auth.login(request,auth_owner)
        request.session['oid']=ownr.id
        messages.add_message(request,messages.INFO,"updated successfully")
    return redirect('view_profile_owner')

@login_required
def view_profile_employee(request):
    emp=employee_reg_tb.objects.filter(id=request.session['eid'])
    return render(request,'employee_profile.html',{'employee':emp})

@login_required
def update_employee_profile(request):
    fname=request.POST['fname']
    lname=request.POST['lname']
    address=request.POST['address']
    dob=request.POST['dob']
    mobile=request.POST['mobile']
    email = request.POST['email']
    username=request.POST['username']
    password=request.POST['password']
    emp=employee_reg_tb.objects.get(id=request.session['eid'])
    auth_emp=User.objects.get(username=emp.username)
    user = Owner_reg_tb.objects.filter(username=username)
    user2 = customer_reg_tb.objects.filter(username=username)
    user3 = Admin_tb.objects.filter(username=username)
    user4 = Manager_tb.objects.filter(username=username)
    user5 = employee_reg_tb.objects.filter(username=username).exclude(id=request.session['eid'])
    if ((user.count() > 0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        messages.add_message(request,messages.INFO,"Username already exist!!!")
    else:
        emp.fname=fname
        emp.lname=lname
        emp.address=address
        emp.dob=dob
        emp.mobile=mobile
        emp.email=email
        emp.usernme=username
        emp.password=password
        emp.save()
        auth_emp.username=username
        auth_emp.set_password(password)
        auth_emp.save()
        auth.authenticate(username=username,password=password)
        auth.login(request,auth_emp)
        request.session['eid']=emp.id
        messages.add_message(request,messages.INFO,"Updated successfully!!!")
    return redirect('view_profile_employee')

def checktime(request):
    crrnt = datetime.datetime.now().strftime('%H:%M')
    crrnt_obj = datetime.datetime.strptime(crrnt, '%H:%M')
    time_en=request.GET['time']
    if 'P' in time_en:
        ptime = int(time_en.split(' ')[0].split(':')[0])
        if ptime != 12:
            ptime = ptime + 12
            s = ':'
            l = [str(ptime), time_en.split(' ')[0].split(':')[1]]
            realtime = s.join(l)
        else:
            realtime = time_en.split(' ')[0]
    else:
        realtime = time_en.split(' ')[0]
    time_en_obj = datetime.datetime.strptime(realtime, '%H:%M')
    if time_en_obj < crrnt_obj:
        return JsonResponse({'status':'not ok'})
    else:
        return JsonResponse({'status':'ok'})

def checkendtime(request):
    stime=request.GET['stime']
    etime=request.GET['etime']
    if stime:
        if 'P' in stime:
            ptime = int(stime.split(' ')[0].split(':')[0])
            if ptime != 12:
                ptime = ptime + 12
                s = ':'
                l = [str(ptime), stime.split(' ')[0].split(':')[1]]
                realtime = s.join(l)
            else:
                realtime = stime.split(' ')[0]
        else:
            realtime = stime.split(' ')[0]
        stime_obj = datetime.datetime.strptime(realtime, '%H:%M')
    
        if 'P' in etime:
            ptime = int(etime.split(' ')[0].split(':')[0])
            if ptime != 12:
                ptime = ptime + 12
                s = ':'
                l = [str(ptime), etime.split(' ')[0].split(':')[1]]
                realtime = s.join(l)
            else:
                realtime = etime.split(' ')[0]
        else:
            realtime = etime.split(' ')[0]
        etime_obj = datetime.datetime.strptime(realtime, '%H:%M') 
        if(etime_obj < stime_obj):
            return JsonResponse({'status':'not ok'})
        else:
            return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no stime'})
