from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from accounts.models import User
from core.storage import upload_private,signed_url
from .forms import MaintenanceRequestForm,MaintenanceUpdateForm
from .models import MaintenanceRequest

def manager(u): return u.is_superuser or u.role in {User.Role.ADMIN,User.Role.GM_HR,User.Role.MANAGER}
@login_required
def maintenance_list(request):
    qs=MaintenanceRequest.objects.select_related('requested_by','assigned_to')
    if not manager(request.user): qs=qs.filter(requested_by=request.user)
    return render(request,'maintenance/list.html',{'tickets':qs,'can_manage':manager(request.user)})
@login_required
def maintenance_create(request):
    form=MaintenanceRequestForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.requested_by=request.user
        if form.cleaned_data.get('attachment'): obj.attachment_object_path=upload_private(form.cleaned_data['attachment'],'maintenance')
        obj.save(); messages.success(request,'Maintenance request submitted.'); return redirect('maintenance_list')
    return render(request,'shared/form_page.html',{'form':form,'title':'New maintenance request','subtitle':'Report an IT, office, facility or equipment issue.'})
@login_required
def maintenance_detail(request,pk):
    obj=get_object_or_404(MaintenanceRequest,pk=pk)
    if not (manager(request.user) or obj.requested_by==request.user): raise PermissionDenied
    form=MaintenanceUpdateForm(request.POST or None,instance=obj)
    if request.method=='POST':
        if not manager(request.user): raise PermissionDenied
        if form.is_valid():
            updated=form.save(commit=False)
            if updated.status in {updated.Status.RESOLVED,updated.Status.CLOSED} and not updated.resolved_at: updated.resolved_at=timezone.now()
            updated.save(); messages.success(request,'Maintenance ticket updated.'); return redirect('maintenance_detail',pk=pk)
    return render(request,'maintenance/detail.html',{'ticket':obj,'form':form,'can_manage':manager(request.user)})
@login_required
def maintenance_file(request,pk):
    obj=get_object_or_404(MaintenanceRequest,pk=pk)
    if not (manager(request.user) or obj.requested_by==request.user): raise PermissionDenied
    return redirect(signed_url(obj.attachment_object_path))
