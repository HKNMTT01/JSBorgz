def notification_summary(request):
    if not request.user.is_authenticated: return {}
    qs=request.user.notifications.all()
    return {'nav_notifications':qs[:5],'unread_notification_count':qs.filter(is_read=False).count()}
