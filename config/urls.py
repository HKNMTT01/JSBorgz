from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
urlpatterns=[
 path('admin/',admin.site.urls),
 path('',include('core.urls')),
 path('accounts/',include('accounts.urls')),
 path('leave/',include('leave_management.urls')),
 path('claims/',include('claims.urls')),
 path('communications/',include('communications.urls')),
 path('attendance/',include('attendance.urls')),
 path('payroll/',include('payroll.urls')),
 path('vouchers/',include('vouchers.urls')),
 path('maintenance/',include('maintenance.urls')),
 path('notifications/',include('notifications.urls')),
 path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
 path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]
