from django.urls import path
from . import views
urlpatterns=[path('reports/',views.reports,name='reports'),path('settings/',views.settings_page,name='settings_page'),path('',views.dashboard,name='dashboard'),path('health/',views.health,name='health')]
