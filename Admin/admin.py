from django.contrib import admin
from Customer.models import *
from Owner.models import *
from Manager.models import *
from Admin.models import *
from Employee.models import *

# Register your models here.
admin.site.register(customer_reg_tb)
admin.site.register(Owner_reg_tb)
admin.site.register(Manager_tb)
admin.site.register(Admin_tb)
admin.site.register(fisher_boat)
admin.site.register(fisher_fish)
admin.site.register(bidding)
admin.site.register(employee_reg_tb)
admin.site.register(Alert_tb)
