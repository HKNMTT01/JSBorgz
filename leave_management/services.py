from datetime import timedelta
from .models import Holiday,LeaveApplication
def working_days(start,end):
    holidays=set(Holiday.objects.filter(date__range=(start,end)).values_list('date',flat=True)); total=0; d=start
    while d<=end:
        if d.weekday()<5 and d not in holidays: total+=1
        d+=timedelta(days=1)
    return total
def approved_days(user,year=None):
    qs=LeaveApplication.objects.filter(employee=user,status=LeaveApplication.Status.APPROVED).exclude(leave_type=LeaveApplication.Type.MEDICAL)
    if year: qs=qs.filter(start_date__year=year)
    return sum(q.total_days for q in qs)
