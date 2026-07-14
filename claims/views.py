from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from accounts.models import User
from core.storage import upload_private,signed_url
from .forms import ClaimForm,ClaimDecisionForm
from .models import Claim
@login_required
def claim_list(request):
    qs=Claim.objects.select_related('employee')
    if not (request.user.is_hr_admin or request.user.is_superuser or request.user.role in {User.Role.GM_FINANCE,User.Role.CEO}): qs=qs.filter(employee=request.user)
    return render(request,'claims/list.html',{'claims':qs})
@login_required
def claim_create(request):
    form=ClaimForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.employee=request.user
        f=form.cleaned_data.get('receipt'); obj.receipt_object_path=upload_private(f,'claim-receipts') if f else ''; obj.save(); messages.success(request,'Claim submitted.'); return redirect('claim_list')
    return render(request,'claims/form.html',{'form':form})
@login_required
def claim_decide(request,pk):
    obj=get_object_or_404(Claim,pk=pk)
    role=request.user.role
    can=(request.user.is_superuser or (obj.status==Claim.Status.PENDING_HR and request.user.is_hr_admin) or (obj.status==Claim.Status.PENDING_FINANCE and role==User.Role.GM_FINANCE) or (obj.status==Claim.Status.PENDING_CEO and role==User.Role.CEO))
    if not can: raise PermissionDenied
    form=ClaimDecisionForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        if form.cleaned_data['decision']=='reject': obj.status=Claim.Status.REJECTED; obj.decided_at=timezone.now()
        elif obj.status==Claim.Status.PENDING_HR: obj.status=Claim.Status.PENDING_FINANCE
        elif obj.status==Claim.Status.PENDING_FINANCE: obj.status=Claim.Status.PENDING_CEO
        else: obj.status=Claim.Status.APPROVED; obj.decided_at=timezone.now()
        obj.current_comment=form.cleaned_data['comment']; obj.save(); messages.success(request,'Claim decision saved.'); return redirect('claim_list')
    return render(request,'claims/decision.html',{'claim':obj,'form':form})
@login_required
def claim_receipt(request,pk):
    obj=get_object_or_404(Claim,pk=pk)
    if not (request.user==obj.employee or request.user.is_hr_admin or request.user.is_superuser or request.user.role in {User.Role.GM_FINANCE,User.Role.CEO}): raise PermissionDenied
    return redirect(signed_url(obj.receipt_object_path))
