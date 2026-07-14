from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import get_object_or_404,redirect,render
from accounts.models import User
from .forms import PayrollPeriodForm,PayslipForm
from .models import PayrollPeriod,Payslip

def _payroll_admin(user): return user.is_superuser or user.role in {User.Role.ADMIN,User.Role.GM_HR,User.Role.GM_FINANCE}
@login_required
def payroll_list(request):
    slips=Payslip.objects.select_related('employee','period')
    if not _payroll_admin(request.user): slips=slips.filter(employee=request.user,status=Payslip.Status.RELEASED)
    totals=slips.aggregate(gross=Sum('basic_salary')+Sum('allowances')+Sum('overtime'), deductions=Sum('deductions')) if _payroll_admin(request.user) else {}
    return render(request,'payroll/list.html',{'slips':slips,'periods':PayrollPeriod.objects.all()[:12],'can_manage':_payroll_admin(request.user),'totals':totals})
@login_required
def payslip_create(request):
    if not _payroll_admin(request.user): raise PermissionDenied
    form=PayslipForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Payslip saved.'); return redirect('payroll_list')
    return render(request,'shared/form_page.html',{'form':form,'title':'Create payslip','subtitle':'Add employee earnings and deductions.'})
@login_required
def payroll_period_create(request):
    if not _payroll_admin(request.user): raise PermissionDenied
    form=PayrollPeriodForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Payroll period created.'); return redirect('payroll_list')
    return render(request,'shared/form_page.html',{'form':form,'title':'New payroll period','subtitle':'Define the salary processing period.'})
@login_required
def payslip_detail(request,pk):
    obj=get_object_or_404(Payslip.objects.select_related('employee','period'),pk=pk)
    if not (_payroll_admin(request.user) or (obj.employee==request.user and obj.status==Payslip.Status.RELEASED)): raise PermissionDenied
    return render(request,'payroll/detail.html',{'payslip':obj})
@login_required
def payslip_release(request,pk):
    if not _payroll_admin(request.user): raise PermissionDenied
    obj=get_object_or_404(Payslip,pk=pk)
    if request.method=='POST': obj.release(); messages.success(request,'Payslip released to employee.')
    return redirect('payslip_detail',pk=pk)
