from django.conf import settings
from django.db import models
class Notification(models.Model):
    class Type(models.TextChoices): INFO='INFO','Information'; APPROVAL='APPROVAL','Approval'; ALERT='ALERT','Alert'; PAYMENT='PAYMENT','Payment'; SYSTEM='SYSTEM','System'
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    title=models.CharField(max_length=180); message=models.TextField(); notification_type=models.CharField(max_length=20,choices=Type.choices,default=Type.INFO)
    action_url=models.CharField(max_length=500,blank=True); is_read=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['recipient','is_read','created_at'])]
    def __str__(self): return self.title
