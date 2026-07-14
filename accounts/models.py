from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name=models.CharField(max_length=120,unique=True)
    code=models.CharField(max_length=20,blank=True)
    is_active=models.BooleanField(default=True)
    def __str__(self): return self.name

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN='ADMIN','Administrator'; EMPLOYEE='EMPLOYEE','Employee'; SUPERVISOR='SUPERVISOR','Supervisor';
        MANAGER='MANAGER','Manager'; GM_HR='GM_HR','GM HR & ESG'; GM_FINANCE='GM_FINANCE','GM Finance'; CEO='CEO','CEO'
    email=models.EmailField(unique=True)
    full_name=models.CharField(max_length=180)
    role=models.CharField(max_length=20,choices=Role.choices,default=Role.EMPLOYEE)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True,related_name='employees')
    position=models.CharField(max_length=120,blank=True)
    phone=models.CharField(max_length=40,blank=True)
    address=models.TextField(blank=True)
    leave_entitlement=models.PositiveIntegerField(default=14)
    profile_object_path=models.CharField(max_length=500,blank=True)
    USERNAME_FIELD='email'; REQUIRED_FIELDS=['username','full_name']
    def __str__(self): return self.full_name or self.email
    @property
    def display_name(self): return self.full_name or self.get_full_name() or self.email
    @property
    def is_hr_admin(self): return self.is_superuser or self.role in {self.Role.ADMIN,self.Role.GM_HR}
