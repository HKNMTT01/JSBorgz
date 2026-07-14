from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
class EmployeeCreateForm(UserCreationForm):
    class Meta:
        model=User; fields=('email','username','full_name','role','department','position','phone','address','leave_entitlement')
class EmployeeUpdateForm(UserChangeForm):
    password=None
    class Meta:
        model=User; fields=('email','username','full_name','role','department','position','phone','address','leave_entitlement','is_active')
