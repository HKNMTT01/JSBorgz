from .models import Notification

def notify(recipient,title,message,notification_type=Notification.Type.INFO,action_url=''):
    if recipient and getattr(recipient,'pk',None):
        return Notification.objects.create(recipient=recipient,title=title,message=message,notification_type=notification_type,action_url=action_url)
