from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
from django.shortcuts import get_object_or_404,redirect,render
from accounts.models import User
from .forms import AttendanceForm
from .models import AttendanceRecord

@login_required
def attendance_list(request):
    qs=AttendanceRecord.objects.select_related('employee')
    if not request.user.is_hr_admin and not request.user.is_superuser: qs=qs.filter(employee=request.user)
    month=request.GET.get('month'); status=request.GET.get('status'); q=request.GET.get('q','').strip()
    if month:
        try: y,m=map(int,month.split('-')); qs=qs.filter(date__year=y,date__month=m)
        except ValueError: pass
    if status: qs=qs.filter(status=status)
    if q: qs=qs.filter(Q(employee__full_name__icontains=q)|Q(employee__email__icontains=q))
    stats=qs.aggregate(total=Count('id'),present=Count('id',filter=Q(status='PRESENT')),late=Count('id',filter=Q(status='LATE')),absent=Count('id',filter=Q(status='ABSENT')))
    return render(request,'attendance/list.html',{'records':qs[:200],'stats':stats,'statuses':AttendanceRecord.Status.choices})

@login_required
def attendance_create(request):
    if not (request.user.is_hr_admin or request.user.is_superuser): return redirect('attendance_list')
    form=AttendanceForm(request.POST or None,initial={'date':date.today()})
    if form.is_valid(): form.save(); messages.success(request,'Attendance record saved.'); return redirect('attendance_list')
    return render(request,'shared/form_page.html',{'form':form,'page_title':'Add attendance','page_eyebrow':'Workforce','submit_label':'Save record'})
