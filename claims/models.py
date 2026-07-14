from django.conf import settings
from django.db import models
from django.utils import timezone
class Claim(models.Model):
    class Status(models.TextChoices):
        PENDING_HR='PENDING_HR','Pending HR Verification'; PENDING_FINANCE='PENDING_FINANCE','Pending Finance Check'; PENDING_CEO='PENDING_CEO','Pending CEO Approval'; APPROVED='APPROVED','Approved'; REJECTED='REJECTED','Rejected'
    employee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='claims')
    title=models.CharField(max_length=180); category=models.CharField(max_length=100); amount=models.DecimalField(max_digits=12,decimal_places=2)
    description=models.TextField(blank=True); receipt_object_path=models.CharField(max_length=500,blank=True)
    status=models.CharField(max_length=30,choices=Status.choices,default=Status.PENDING_HR)
    current_comment=models.TextField(blank=True); submitted_at=models.DateTimeField(default=timezone.now); decided_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['employee','status']),models.Index(fields=['status','submitted_at'])]
    def __str__(self): return f'{self.employee}: {self.title}'
