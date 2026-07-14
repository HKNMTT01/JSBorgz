from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Department
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering=('email',); list_display=('email','full_name','role','department','is_active')
    fieldsets=UserAdmin.fieldsets+(('HR profile',{'fields':('full_name','role','department','position','phone','address','leave_entitlement','profile_object_path')}),)
    add_fieldsets=UserAdmin.add_fieldsets+(('HR profile',{'fields':('email','full_name','role','department','position','leave_entitlement')}),)
admin.site.register(Department)
