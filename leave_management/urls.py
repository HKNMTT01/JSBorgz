from django.urls import path
from . import views
urlpatterns=[path('',views.leave_list,name='leave_list'),path('apply/',views.leave_apply,name='leave_apply'),path('<int:pk>/decide/',views.leave_decide,name='leave_decide'),path('<int:pk>/document/',views.leave_document,name='leave_document')]
