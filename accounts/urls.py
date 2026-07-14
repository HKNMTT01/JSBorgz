from django.urls import path
from . import views
urlpatterns=[path('profile/',views.my_profile,name='my_profile'),path('employees/<int:pk>/',views.employee_detail,name='employee_detail'),path('employees/',views.employee_list,name='employee_list'),path('employees/add/',views.employee_create,name='employee_create'),path('employees/<int:pk>/edit/',views.employee_edit,name='employee_edit')]
