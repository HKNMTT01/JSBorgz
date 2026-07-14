from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q,Sum
from django.shortcuts import render
from accounts.models import User,Department
from leave_management.models import LeaveApplication
from claims.models import Claim
from communications.models import Notice,Policy

@login_required
def dashboard(request):
    u=request.user
    context={'notices':Notice.objects.filter(is_published=True)[:5],'policies':Policy.objects.filter(is_active=True)[:5]}
    if u.is_hr_admin or u.is_superuser:
        from attendance.models import AttendanceRecord
        context.update(
            admin_view=True,
            employee_count=User.objects.filter(is_active=True).count(),
            department_count=Department.objects.filter(is_active=True).count(),
            pending_leave_count=LeaveApplication.objects.filter(status__in=[LeaveApplication.Status.PENDING_RECOMMENDER,LeaveApplication.Status.PENDING_APPROVER]).count(),
            pending_claim_count=Claim.objects.exclude(status__in=[Claim.Status.APPROVED,Claim.Status.REJECTED]).count(),
            recent_leaves=LeaveApplication.objects.select_related('employee')[:6],
            recent_claims=Claim.objects.select_related('employee')[:6],
            department_summary=Department.objects.annotate(total=Count('employees',filter=Q(employees__is_active=True))).order_by('-total')[:6],
            attendance_today=AttendanceRecord.objects.filter(date__exact=__import__('datetime').date.today()).values('status').annotate(total=Count('id')),
            recent_employees=User.objects.filter(is_active=True).select_related('department').order_by('-date_joined')[:5],
        )
    else:
        approved=LeaveApplication.objects.filter(employee=u,status=LeaveApplication.Status.APPROVED).aggregate(total=Sum('total_days'))['total'] or 0
        context.update(admin_view=False,my_leaves=LeaveApplication.objects.filter(employee=u)[:5],my_claims=Claim.objects.filter(employee=u)[:5],leave_used=approved,leave_remaining=max(0,u.leave_entitlement-approved))
    return render(request,'core/dashboard.html',context)

def health(request):
    from django.http import JsonResponse
    from django.db import connection
    with connection.cursor() as c: c.execute('SELECT 1'); ok=c.fetchone()[0]
    return JsonResponse({'status':'ok','database':ok})

@login_required
def reports(request):
    from attendance.models import AttendanceRecord
    leave_by_status=list(LeaveApplication.objects.values('status').annotate(total=Count('id')).order_by('status'))
    claim_by_status=list(Claim.objects.values('status').annotate(total=Count('id')).order_by('status'))
    dept_headcount=list(Department.objects.annotate(total=Count('employees',filter=Q(employees__is_active=True))).values('name','total').order_by('-total')[:10])
    attendance_by_status=list(AttendanceRecord.objects.values('status').annotate(total=Count('id')).order_by('status'))
    return render(request,'core/reports.html',{'leave_by_status':leave_by_status,'claim_by_status':claim_by_status,'dept_headcount':dept_headcount,'attendance_by_status':attendance_by_status})

@login_required
def settings_page(request): return render(request,'core/settings.html')
