from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from .models import Notification
@login_required
def notification_list(request): return render(request,'notifications/list.html',{'notifications':request.user.notifications.all()})
@login_required
def notification_read(request,pk):
    obj=get_object_or_404(Notification,pk=pk,recipient=request.user); obj.is_read=True; obj.save(update_fields=['is_read'])
    return redirect(obj.action_url or 'notification_list')
@login_required
def notification_read_all(request):
    if request.method=='POST': request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notification_list')
