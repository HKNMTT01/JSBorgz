from django.urls import path
from . import views
urlpatterns=[
 path('notices/',views.notice_list,name='notice_list'),path('notices/add/',views.notice_create,name='notice_create'),path('notices/<int:pk>/attachment/',views.notice_attachment,name='notice_attachment'),
 path('policies/',views.policy_list,name='policy_list'),path('policies/add/',views.policy_create,name='policy_create'),path('policies/<int:pk>/file/',views.policy_file,name='policy_file'),
 path('circulars/',views.circular_list,name='circular_list'),path('circulars/add/',views.circular_create,name='circular_create'),path('circulars/<int:pk>/file/',views.circular_file,name='circular_file'),
]
