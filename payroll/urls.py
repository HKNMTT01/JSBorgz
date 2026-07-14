from django.urls import path
from . import views
urlpatterns=[path('',views.payroll_list,name='payroll_list'),path('period/new/',views.payroll_period_create,name='payroll_period_create'),path('new/',views.payslip_create,name='payslip_create'),path('<int:pk>/',views.payslip_detail,name='payslip_detail'),path('<int:pk>/release/',views.payslip_release,name='payslip_release')]
