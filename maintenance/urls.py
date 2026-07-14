from django.urls import path
from . import views
urlpatterns=[path('',views.maintenance_list,name='maintenance_list'),path('new/',views.maintenance_create,name='maintenance_create'),path('<int:pk>/',views.maintenance_detail,name='maintenance_detail'),path('<int:pk>/attachment/',views.maintenance_file,name='maintenance_file')]
