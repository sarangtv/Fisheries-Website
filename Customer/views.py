from django.shortcuts import render,redirect
from Customer.models import *
from Admin.models import *
from Manager.models import *
from Owner.models import *
import datetime
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def Customer_registration(request):
    return render(request,'customer_reg.html')

def Customer_reg_action(request):
    fname=request.POST['fname']
    lname = request.POST['lname']
    address = request.POST['address']
    dob= request.POST['dob']
    mobile=request.POST['mobile']
    username=request.POST['username']
    password=request.POST['password']
    user=customer_reg_tb.objects.filter(username=username)
    user2 = Owner_reg_tb.objects.filter(username=username)
    user3 = Admin_tb.objects.filter(username=username)
    user4 = Manager_tb.objects.filter(username=username)
    user5 = employee_reg_tb.objects.filter(username=username)
    if((user.count()>0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        messages.add_message(request,messages.INFO,'Username already exist!!!')
    else:
        user=customer_reg_tb(fname=fname,lname=lname,address=address,dob=dob,mobile=mobile,username=username,password=password)
        user.save()
        user=User.objects.create_user(username=username,password=password)
        user.save()
        messages.add_message(request,messages.INFO,'Registration successful')
    return redirect('Customer_registration')

@login_required
def view_auctions(request):
    date=datetime.date.today()
    fish=fisher_fish.objects.filter(date=date).order_by('-id')
    return render(request, 'view_auctions.html', {'fs': fish})

@login_required
def biddingg(request,fish_id):
    fish=bidding.objects.filter(fish_id=fish_id).order_by('-price')
    return render(request, 'bidding.html',{'fsh': fish,'fish_id':fish_id})

@login_required
def bidding_action(request):
    price=float(request.POST['price'])
    fish_id=request.POST['fish_id']
    cust_id=request.session['cid']
    cust=customer_reg_tb.objects.get(id=cust_id)
    fish=fisher_fish.objects.get(id=fish_id)
    bid = bidding.objects.filter(fish_id=fish_id).order_by('-price')
    if(price < fish.price):
        messages.add_message(request,messages.INFO,"Price less than minimum price")
        return redirect('view_auctions')
    else:
        bid_obj=bidding(price=price,cust_id=cust,fish_id=fish)
        bid_obj.save()
        messages.add_message(request,messages.INFO,"Submitted Successfully")
        return redirect('view_auctions')
    
def update_fish_status(request):
    date = str(datetime.date.today())
    crrnt = datetime.datetime.now().strftime('%H:%M')
    crrnt_obj = datetime.datetime.strptime(crrnt, '%H:%M')
    
    fish=fisher_fish.objects.filter(status__in=['pending','Ongoing'])
    for f in fish:
        fyear=int(f.date.split('-')[0])
        fmonth=int(f.date.split('-')[1])
        fday=int(f.date.split('-')[2])
        fdate=datetime.datetime(fyear,fmonth,fday)
        
        pyear=int(date.split('-')[0])
        pmonth=int(date.split('-')[1])
        pday=int(date.split('-')[2])
        pdate=datetime.datetime(pyear,pmonth,pday)
        
        if fdate < pdate:
            f.status="expired"
            f.save()
            
    fish = fisher_fish.objects.filter(date=date, status='pending')
    for f in fish:
        start_time = f.start_time
        if 'P' in start_time:
            ptime = int(start_time.split(' ')[0].split(':')[0])
            if ptime != 12:
                ptime = ptime + 12
                s = ':'
                l = [str(ptime), start_time.split(' ')[0].split(':')[1]]
                realtime = s.join(l)
            else:
                realtime = start_time.split(' ')[0]
        else:
            realtime = start_time.split(' ')[0]
        start_time = datetime.datetime.strptime(realtime, '%H:%M')
        if crrnt_obj >= start_time:
            fish = fisher_fish.objects.filter(id=f.id).update(status='Ongoing')
    fish = fisher_fish.objects.filter(date=date, status='Ongoing')
    for f in fish:
        endtime=f.end_time

        if 'P' in endtime:
            ptime=int(endtime.split(' ')[0].split(':')[0])
            if ptime != 12:
                ptime=ptime+12
                s=':'
                l=[str(ptime),endtime.split(' ')[0].split(':')[1]]
                realtime=s.join(l)
            else:
                realtime=endtime.split(' ')[0]
        else:

            realtime=endtime.split(' ')[0]
        print(realtime,"yyy")
        endtime=datetime.datetime.strptime(realtime,'%H:%M')
        if crrnt_obj>=endtime:
            fish=fisher_fish.objects.filter(id=f.id).update(status='expired')
    fish_exp=fisher_fish.objects.filter(status='expired')
    for fsh in fish_exp:
        bid=bidding.objects.filter(fish_id=fsh.id).order_by('-price')
        if bid.count()>0:
            bid_obj = bid[0]
            bid_obj.status="Won"
            bid_obj.save()
            bid=bidding.objects.filter(fish_id=fsh.id).exclude(id=bid_obj.id).update(status="Failed")
    if request.GET.get('page')=='1':
        fish = fisher_fish.objects.filter(date=date).order_by('-id')
        return render(request,'get_auctions.html',{'fs':fish})
    elif request.GET.get('page')=='2':
        print(request.GET.get('page'))
        fish = bidding.objects.filter(cust_id=request.session['cid']).order_by('-id')
        return render(request,'get_mybidding.html',{'fish':fish})
    elif request.GET.get('page')=='3':
        details = fisher_fish.objects.all().order_by('-id')
        return render(request, 'get_auctions_manager.html', {'dtls': details})
    else:
        fish=''
        if 'oid' in request.session:
            fish=fisher_fish.objects.filter(owner_id=request.session['oid']).order_by('-id')
        return render(request, 'get_auctions_owner.html', {'fish': fish})

@login_required    
def view_profile(request):
    cust=customer_reg_tb.objects.filter(id=request.session['cid'])
    return render(request,'customer_profile.html',{'customer':cust})

@login_required
def update_customer_profile(request):
    fname=request.POST['fname']
    lname=request.POST['lname']
    address=request.POST['address']
    dob=request.POST['dob']
    mobile=request.POST['mobile']
    username=request.POST['username']
    password=request.POST['password']
    cust=customer_reg_tb.objects.get(id=request.session['cid'])
    auth_customer=User.objects.get(username=cust.username)
    user=customer_reg_tb.objects.filter(username=username).exclude(id=request.session['cid'])
    user2 = Owner_reg_tb.objects.filter(username=username)
    user3 = Admin_tb.objects.filter(username=username)
    user4 = Manager_tb.objects.filter(username=username)
    user5 = employee_reg_tb.objects.filter(username=username)
    if((user.count()>0)or(user2.count()>0)or(user3.count()>0)or(user4.count()>0)or(user5.count()>0)):
        messages.add_message(request,messages.INFO,'Username already exist!!!')
    else:
        cust.fname=fname
        cust.lname=lname
        cust.address=address
        cust.dob=dob
        cust.mobile=mobile
        cust.usernme=username
        cust.password=password
        cust.save()
        auth_customer.username=username
        auth_customer.set_password(password)
        auth_customer.save()
        auth_customer=auth.authenticate(username=username,password=password)
        auth.login(request,auth_customer)
        request.session['cid']=cust.id
        messages.add_message(request,messages.INFO,"updated successfully!!!")
    return redirect('view_profile')

@login_required
def my_auctions(request):
    fish=bidding.objects.filter(cust_id=request.session['cid']).order_by('-id')
    return render(request,'my_auctions.html',{'fish':fish})

@login_required
def view_details(request,v_id):
    fish=bidding.objects.get(id=v_id)
    return render(request,'my_auctions_details.html',{'fs':fish})

@login_required
def write_complaints(request):
    complaints=complaint_tb.objects.filter(cust_id=request.session['cid'])
    return render(request,'complaint.html',{'complaints':complaints})

@login_required
def viewReply(request,cid):
    replies=reply_tb.objects.filter(compl_id=cid)
    return render(request,'view_reply.html',{'reply':replies})

@login_required
def complaint_action(request):
    cust=customer_reg_tb.objects.get(id=request.session['cid'])
    subject=request.POST['subject']
    complaint=request.POST['complaint']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime("%H:%M")
    comp=complaint_tb(cust_id=cust,subject=subject,complaint=complaint,date=date,time=time)
    comp.save()
    messages.add_message(request,messages.INFO,"Complaint added!!!")
    return redirect('write_complaints')
