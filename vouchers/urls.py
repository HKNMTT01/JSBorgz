from django.urls import path
from . import views
urlpatterns=[path('',views.voucher_list,name='voucher_list'),path('new/',views.voucher_create,name='voucher_create'),path('<int:pk>/',views.voucher_detail,name='voucher_detail'),path('<int:pk>/<str:action>/',views.voucher_action,name='voucher_action'),path('<int:pk>/file/<str:kind>/',views.voucher_file,name='voucher_file')]
