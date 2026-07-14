from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Holiday(models.Model):
    date=models.DateField(unique=True); name=models.CharField(max_length=160)
    class Meta: ordering=['date']
    def __str__(self): return f'{self.date} — {self.name}'

class LeaveApplication(models.Model):
    class Type(models.TextChoices):
        ANNUAL='ANNUAL','Annual Leave'; MEDICAL='MEDICAL','Medical Leave'; EMERGENCY='EMERGENCY','Emergency Leave'; UNPAID='UNPAID','Unpaid Leave'; OTHER='OTHER','Other'
    class Status(models.TextChoices):
        DRAFT='DRAFT','Draft'; PENDING_RECOMMENDER='PENDING_RECOMMENDER','Pending Recommender'; PENDING_APPROVER='PENDING_APPROVER','Pending Approver'; APPROVED='APPROVED','Approved'; REJECTED='REJECTED','Rejected'; CANCELLED='CANCELLED','Cancelled'
    employee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='leave_applications')
    leave_type=models.CharField(max_length=20,choices=Type.choices)
    start_date=models.DateField(); end_date=models.DateField(); total_days=models.PositiveIntegerField(default=0)
    reason=models.TextField(); contact_address=models.TextField(blank=True); contact_phone=models.CharField(max_length=40,blank=True)
    support_object_path=models.CharField(max_length=500,blank=True)
    recommender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='leave_recommendations')
    approver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='leave_approvals')
    status=models.CharField(max_length=30,choices=Status.choices,default=Status.PENDING_RECOMMENDER)
    recommender_comment=models.TextField(blank=True); approver_comment=models.TextField(blank=True)
    submitted_at=models.DateTimeField(default=timezone.now); decided_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['employee','status']),models.Index(fields=['start_date','end_date'])]
    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date: raise ValidationError('End date cannot be earlier than start date.')
    def __str__(self): return f'{self.employee} - {self.get_leave_type_display()} ({self.start_date})'
