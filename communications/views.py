from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect,render
from accounts.models import User
from core.decorators import roles_required
from core.storage import upload_private,signed_url
from .forms import NoticeForm,PolicyForm
from .models import Notice,Policy
@login_required
def notice_list(request): return render(request,'communications/notices.html',{'notices':Notice.objects.filter(is_published=True)})
@roles_required(User.Role.ADMIN,User.Role.GM_HR)
def notice_create(request):
    form=NoticeForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.created_by=request.user; f=form.cleaned_data.get('attachment'); obj.attachment_object_path=upload_private(f,'notices') if f else ''; obj.save(); messages.success(request,'Notice published.'); return redirect('notice_list')
    return render(request,'communications/form.html',{'form':form,'title':'Publish notice'})
@login_required
def notice_attachment(request,pk): return redirect(signed_url(get_object_or_404(Notice,pk=pk).attachment_object_path))
@login_required
def policy_list(request): return render(request,'communications/policies.html',{'policies':Policy.objects.filter(is_active=True)})
@roles_required(User.Role.ADMIN,User.Role.GM_HR)
def policy_create(request):
    form=PolicyForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.uploaded_by=request.user; obj.file_object_path=upload_private(form.cleaned_data['file'],'policies'); obj.save(); messages.success(request,'Policy uploaded.'); return redirect('policy_list')
    return render(request,'communications/form.html',{'form':form,'title':'Upload policy'})
@login_required
def policy_file(request,pk): return redirect(signed_url(get_object_or_404(Policy,pk=pk,is_active=True).file_object_path))

from .models import Circular
from .forms import CircularForm
@login_required
def circular_list(request):
    qs=Circular.objects.select_related('department','created_by').filter(is_published=True)
    if not request.user.is_hr_admin and not request.user.is_superuser:
        filters=models.Q(audience=Circular.Audience.ALL)
        if request.user.department_id:
            filters |= models.Q(audience=Circular.Audience.DEPARTMENT,department=request.user.department)
        if request.user.role in {User.Role.MANAGER,User.Role.GM_HR,User.Role.GM_FINANCE,User.Role.CEO,User.Role.ADMIN}:
            filters |= models.Q(audience=Circular.Audience.MANAGEMENT)
        qs=qs.filter(filters)
    return render(request,'communications/circulars.html',{'circulars':qs})
@login_required
def circular_create(request):
    if not request.user.is_hr_admin: raise PermissionDenied
    form=CircularForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.created_by=request.user; obj.file_object_path=upload_private(form.cleaned_data['file'],'circulars'); obj.save(); messages.success(request,'Circular published.'); return redirect('circular_list')
    return render(request,'shared/form_page.html',{'form':form,'title':'Publish circular','subtitle':'Issue an official company circular with a private document.'})
@login_required
def circular_file(request,pk):
    obj=get_object_or_404(Circular,pk=pk)
    return redirect(signed_url(obj.file_object_path))
