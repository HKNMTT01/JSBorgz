from django.contrib import admin
from .models import PayrollPeriod,Payslip
admin.site.register(PayrollPeriod)
@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin): list_display=('employee','period','status','basic_salary','deductions'); list_filter=('status','period')
