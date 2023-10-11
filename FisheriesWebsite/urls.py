"""FisheriesWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from Admin import views as admin_view
from Manager import views as manager_view
from Customer import views as customer_view
from Employee import views as employee_view
from Owner import views as owner_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',admin_view.index,name='index'),
    url(r'^Customer_registration/',customer_view.Customer_registration,name='Customer_registration'),
    url(r'^Customer_reg_action/',customer_view.Customer_reg_action,name='Customer_reg_action'),
    url(r'^Owner_registration/',owner_view.Owner_registration,name='Owner_registration'),
    url(r'^Owner_reg_action/',owner_view.Owner_reg_action,name='Owner_reg_action'),
    url(r'^Login/',admin_view.Login,name='Login'),
    url(r'^login_action/',admin_view.login_action,name='login_action'),
    url(r'^view_owners/',admin_view.view_owners,name='view_owners'),
    url(r'^Approve/(?P<oid>\d+)/$',admin_view.Approve,name='Approve'),
    url(r'^Reject/(?P<oid>\d+)/$',admin_view.Reject,name='Reject'),
    url(r'^add_boat/', owner_view.add_boat, name='add_boat'),
    url(r'^add_boat_action/', owner_view.add_boat_action, name='add_boat_action'),
    url(r'^add_employee/', owner_view.add_employee, name='add_employee'),
    url(r'^add_employee_action/', owner_view.add_employee_action, name='add_employee_action'),
    url(r'^view_boats/',owner_view.view_boats,name='view_boats'),
    url(r'^Update_boat/(?P<bid>\d+)/$', owner_view.Update_boat, name='Update_boat'),
    url(r'^Update_boat_action/',owner_view.Update_boat_action,name='Update_boat_action'),
    url(r'^Delete_boat/(?P<bid>\d+)/$', owner_view.Delete_boat, name='Delete_boat'),
    url(r'^view_employees/',owner_view.view_employees,name='view_employees'),
    url(r'^Delete_employee/(?P<eid>\d+)/$', owner_view.Delete_employee, name='Delete_employee'),
    url(r'^view_employees_admin/(?P<oid>\d+)/$',admin_view.view_employees_admin,name='view_employees_admin'),
    url(r'^add_fish/', owner_view.add_fish, name='add_fish'),
    url(r'^add_fish_action/', owner_view.add_fish_action, name='add_fish_action'),
    url(r'^view_fish/', owner_view.view_fish, name='view_fish'),
    url(r'^delete_fish/(?P<fid>\d+)/$', owner_view.delete_fish, name='delete_fish'),
    url(r'^update_fish/(?P<fid>\d+)/$', owner_view.update_fish, name='update_fish'),
    url(r'^update_fish_action/', owner_view.update_fish_action, name='update_fish_action'),
    url(r'^view_auctions/', customer_view.view_auctions, name='view_auctions'),
    url(r'^biddingg/(?P<fish_id>\d+)/$', customer_view.biddingg, name='biddingg'),
    url(r'^bidding_action/', customer_view.bidding_action, name='bidding_action'),
    url(r'^fish_view_auction/(?P<fish_id>\d+)/$', owner_view.fish_view_auction, name='fish_view_auction'),
    url(r'^cust_details/(?P<cust_id>\d+)/(?P<fish_id>\d+)/$', owner_view.cust_details, name='cust_details'),
    url(r'^update_fish_status/', customer_view.update_fish_status, name='update_fish_status'),
    url(r'^view_profile/', customer_view.view_profile, name='view_profile'),
    url(r'^update_customer_profile/', customer_view.update_customer_profile, name='update_customer_profile'),
    url(r'^view_profile_owner/', owner_view.view_profile_owner, name='view_profile_owner'),
    url(r'^update_owner_profile/', owner_view.update_owner_profile, name='update_owner_profile'),
    url(r'^view_profile_employee/', owner_view.view_profile_employee, name='view_profile_employee'),
    url(r'^update_employee_profile/', owner_view.update_employee_profile, name='update_employee_profile'),
    url(r'^alert_manager/', employee_view.alert_manager, name='alert_manager'),
    url(r'^view_alerts/', manager_view.view_alerts, name='view_alerts'),
    url(r'^forgor_password/', admin_view.forgot_password, name='forgot_password'),
    url(r'^user_validation_action/', admin_view.user_validation_action, name='user_validation_action'),
    url(r'^user_validation2_action/', admin_view.user_validation2_action, name='user_validation2_action'),
    url(r'^forgor_password_action/', admin_view.forgot_password_action, name='forgot_password_action'),
    url(r'^my_auctions/', customer_view.my_auctions, name='my_auctions'),
    url(r'^view_details/(?P<v_id>\d+)/$', customer_view.view_details, name='view_details'),
    url(r'^view_auctions_manager/', manager_view.view_auctions_manager, name='view_auctions_manager'),
    url(r'^view_details_manager/(?P<v_id>\d+)/$', manager_view.view_details_manager, name='view_details_manager'),
    url(r'^write_complaints/', customer_view.write_complaints, name='write_complaints'),
    url(r'^complaint_action/', customer_view.complaint_action, name='complaint_action'),
    url(r'^view_complaints/', manager_view.view_complaints, name='view_complaints'),
    url(r'^complaint_detail/(?P<comp_id>\d+)/$', manager_view.complaint_detail, name='complaint_detail'),
    url(r'^reply_action/', manager_view.reply_action, name='reply_action'),
    url(r'^alertEmployeeDetails/(?P<eid>\d+)/$', manager_view.alertEmployeeDetails, name='alertEmployeeDetails'),
    url(r'^readAlert/(?P<aid>\d+)/$', manager_view.readAlert, name='readAlert'),
    url(r'^viewReply/(?P<cid>\d+)/$', customer_view.viewReply, name='viewReply'),
    url(r'^checktime/',owner_view.checktime,name='checktime'),
    url(r'^checkendtime/',owner_view.checkendtime,name='checkendtime'),
    url(r'^checkUsername/',admin_view.checkUsername,name='checkUsername'),
    url(r'^logout/', admin_view.logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
