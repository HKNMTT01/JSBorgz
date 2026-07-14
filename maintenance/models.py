from django.conf import settings
from django.db import models
class MaintenanceRequest(models.Model):
    class Priority(models.TextChoices): LOW='LOW','Low'; MEDIUM='MEDIUM','Medium'; HIGH='HIGH','High'; CRITICAL='CRITICAL','Critical'
    class Status(models.TextChoices): OPEN='OPEN','Open'; ASSIGNED='ASSIGNED','Assigned'; IN_PROGRESS='IN_PROGRESS','In Progress'; RESOLVED='RESOLVED','Resolved'; CLOSED='CLOSED','Closed'
    ticket_no=models.CharField(max_length=40,unique=True); title=models.CharField(max_length=180); category=models.CharField(max_length=100)
    location=models.CharField(max_length=180,blank=True); description=models.TextField(); priority=models.CharField(max_length=20,choices=Priority.choices,default=Priority.MEDIUM)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    requested_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='maintenance_requests')
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='maintenance_assignments')
    attachment_object_path=models.CharField(max_length=500,blank=True); resolution_notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True); resolved_at=models.DateTimeField(null=True,blank=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return self.ticket_no
