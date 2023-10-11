from django.db import models
from Owner.models import *

# Create your models here.
class Alert_tb(models.Model):
    empl_id = models.ForeignKey(employee_reg_tb,on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    status=models.CharField(max_length=10,default='pending')
