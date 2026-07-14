from django.urls import path
from . import views
urlpatterns=[path('',views.claim_list,name='claim_list'),path('submit/',views.claim_create,name='claim_create'),path('<int:pk>/decide/',views.claim_decide,name='claim_decide'),path('<int:pk>/receipt/',views.claim_receipt,name='claim_receipt')]
