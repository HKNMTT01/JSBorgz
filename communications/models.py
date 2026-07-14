from django.conf import settings
from django.db import models
class Notice(models.Model):
    title=models.CharField(max_length=180); content=models.TextField(); attachment_object_path=models.CharField(max_length=500,blank=True)
    is_published=models.BooleanField(default=True); created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']
class Policy(models.Model):
    title=models.CharField(max_length=180); version=models.CharField(max_length=40,blank=True); file_object_path=models.CharField(max_length=500)
    is_active=models.BooleanField(default=True); uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']

class Circular(models.Model):
    class Audience(models.TextChoices): ALL='ALL','All Employees'; MANAGEMENT='MANAGEMENT','Management'; HR='HR','HR & ESG'; FINANCE='FINANCE','Finance'; DEPARTMENT='DEPARTMENT','Specific Department'
    reference_no=models.CharField(max_length=60,unique=True)
    title=models.CharField(max_length=220); summary=models.TextField(blank=True)
    audience=models.CharField(max_length=20,choices=Audience.choices,default=Audience.ALL)
    department=models.ForeignKey('accounts.Department',on_delete=models.SET_NULL,null=True,blank=True,related_name='circulars')
    effective_date=models.DateField(); expiry_date=models.DateField(null=True,blank=True)
    file_object_path=models.CharField(max_length=500)
    is_published=models.BooleanField(default=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='created_circulars')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-effective_date','-created_at']
    def __str__(self): return f'{self.reference_no} - {self.title}'
