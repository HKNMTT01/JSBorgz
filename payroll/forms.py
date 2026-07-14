from django import forms
from .models import PayrollPeriod,Payslip
class PayrollPeriodForm(forms.ModelForm):
    class Meta: model=PayrollPeriod; fields=['name','start_date','end_date','pay_date']; widgets={k:forms.DateInput(attrs={'type':'date'}) for k in ['start_date','end_date','pay_date']}
class PayslipForm(forms.ModelForm):
    class Meta: model=Payslip; fields=['employee','period','basic_salary','allowances','overtime','deductions','employer_contribution','remarks','status']
