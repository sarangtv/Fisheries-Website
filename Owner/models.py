from django.db import models

# Create your models here.
class Owner_reg_tb(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    address=models.CharField(max_length=40)
    dob=models.CharField(max_length=20)
    mobile=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
    proof=models.FileField(default='No proof')

class fisher_boat(models.Model):
    name = models.CharField(max_length=20)
    regno = models.CharField(max_length=20)
    photo = models.FileField()
    owner_id = models.ForeignKey(Owner_reg_tb,on_delete=models.CASCADE)
    no_of_empl=models.IntegerField()

class employee_reg_tb(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    address=models.CharField(max_length=40)
    dob=models.CharField(max_length=20)
    mobile=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    username=models.CharField(max_length=20,default='No username')
    password=models.CharField(max_length=20,default='No password')
    boat_id=models.ForeignKey(fisher_boat,on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Owner_reg_tb, on_delete=models.CASCADE,default=1)

class fisher_fish(models.Model):
    name=models.CharField(max_length=20)
    photo=models.FileField()
    quantity=models.CharField(max_length=20)
    price=models.FloatField()
    start_time=models.CharField(max_length=20,default="No time")
    end_time=models.CharField(max_length=20,default="No time")
    status=models.CharField(max_length=20,default="pending")
    date=models.CharField(max_length=10,default="No date")
    owner_id = models.ForeignKey(Owner_reg_tb,on_delete=models.CASCADE)




