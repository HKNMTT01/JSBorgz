from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404,redirect,render
from .models import User
from .forms import EmployeeCreateForm,EmployeeUpdateForm
from core.decorators import roles_required
@roles_required(User.Role.ADMIN,User.Role.GM_HR)
def employee_list(request): return render(request,'accounts/employee_list.html',{'employees':User.objects.select_related('department').order_by('full_name')})
@roles_required(User.Role.ADMIN,User.Role.GM_HR)
def employee_create(request):
    form=EmployeeCreateForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Employee account created.'); return redirect('employee_list')
    return render(request,'accounts/employee_form.html',{'form':form,'title':'Add employee'})
@roles_required(User.Role.ADMIN,User.Role.GM_HR)
def employee_edit(request,pk):
    employee=get_object_or_404(User,pk=pk); form=EmployeeUpdateForm(request.POST or None,instance=employee)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Employee updated.'); return redirect('employee_list')
    return render(request,'accounts/employee_form.html',{'form':form,'title':'Edit employee'})


@login_required
def employee_detail(request, pk):
    employee=get_object_or_404(User.objects.select_related('department'),pk=pk)
    if not (request.user.is_hr_admin or request.user.is_superuser or request.user.pk==employee.pk):
        messages.error(request,'You do not have permission to view this profile.'); return redirect('dashboard')
    from leave_management.models import LeaveApplication
    from claims.models import Claim
    from attendance.models import AttendanceRecord
    return render(request,'accounts/employee_detail.html',{'employee':employee,'leaves':LeaveApplication.objects.filter(employee=employee)[:8],'claims':Claim.objects.filter(employee=employee)[:8],'attendance':AttendanceRecord.objects.filter(employee=employee)[:10]})

@login_required
def my_profile(request):
    return employee_detail(request, request.user.pk)
