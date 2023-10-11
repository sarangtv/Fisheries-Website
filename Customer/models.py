from django.db import models
from Owner.models import *

# Create your models here.
class customer_reg_tb(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    address=models.CharField(max_length=40)
    dob=models.CharField(max_length=20)
    mobile=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
class bidding(models.Model):
    price=models.FloatField()
    cust_id=models.ForeignKey(customer_reg_tb,on_delete=models.CASCADE)
    fish_id=models.ForeignKey(fisher_fish,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default="pending")
class complaint_tb(models.Model):
    subject=models.CharField(max_length=40)
    complaint=models.CharField(max_length=100)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    cust_id=models.ForeignKey(customer_reg_tb,on_delete=models.CASCADE,default=1)
    status=models.CharField(max_length=10,default='pending')
class reply_tb(models.Model):
    subject=models.CharField(max_length=20)
    reply=models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    compl_id=models.ForeignKey(complaint_tb,on_delete=models.CASCADE)

