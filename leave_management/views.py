from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from core.storage import upload_private,signed_url
from .forms import LeaveApplicationForm,DecisionForm
from .models import LeaveApplication
from .services import working_days,approved_days
@login_required
def leave_list(request):
    qs=LeaveApplication.objects.select_related('employee','recommender','approver')
    if not request.user.is_hr_admin and not request.user.is_superuser: qs=qs.filter(employee=request.user)
    return render(request,'leave_management/list.html',{'leaves':qs})
@login_required
def leave_apply(request):
    form=LeaveApplicationForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.employee=request.user; obj.total_days=working_days(obj.start_date,obj.end_date)
        if obj.leave_type!=LeaveApplication.Type.MEDICAL and approved_days(request.user,obj.start_date.year)+obj.total_days>request.user.leave_entitlement:
            form.add_error(None,'This request exceeds your available annual leave balance.')
        else:
            f=form.cleaned_data.get('support_document'); obj.support_object_path=upload_private(f,'leave-documents') if f else ''; obj.save(); messages.success(request,'Leave application submitted.'); return redirect('leave_list')
    return render(request,'leave_management/form.html',{'form':form})
@login_required
def leave_decide(request,pk):
    obj=get_object_or_404(LeaveApplication,pk=pk); allowed=request.user.is_hr_admin or request.user.is_superuser or request.user in {obj.recommender,obj.approver}
    if not allowed: raise PermissionDenied
    form=DecisionForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        approve=form.cleaned_data['decision']=='approve'; comment=form.cleaned_data['comment']
        if not approve: obj.status=LeaveApplication.Status.REJECTED; obj.decided_at=timezone.now()
        elif obj.status==LeaveApplication.Status.PENDING_RECOMMENDER: obj.status=LeaveApplication.Status.PENDING_APPROVER; obj.recommender_comment=comment
        else: obj.status=LeaveApplication.Status.APPROVED; obj.approver_comment=comment; obj.decided_at=timezone.now()
        obj.save(); messages.success(request,'Leave decision saved.'); return redirect('leave_list')
    return render(request,'leave_management/decision.html',{'leave':obj,'form':form})
@login_required
def leave_document(request,pk):
    obj=get_object_or_404(LeaveApplication,pk=pk)
    if not (request.user==obj.employee or request.user.is_hr_admin or request.user.is_superuser or request.user in {obj.recommender,obj.approver}): raise PermissionDenied
    return redirect(signed_url(obj.support_object_path))
