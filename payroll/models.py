from django.conf import settings
from django.db import models
from django.utils import timezone
class PayrollPeriod(models.Model):
    name=models.CharField(max_length=100)
    start_date=models.DateField(); end_date=models.DateField(); pay_date=models.DateField()
    is_closed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-pay_date']; unique_together=('start_date','end_date')
    def __str__(self): return self.name
class Payslip(models.Model):
    class Status(models.TextChoices): DRAFT='DRAFT','Draft'; REVIEWED='REVIEWED','Reviewed'; RELEASED='RELEASED','Released'
    employee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='payslips')
    period=models.ForeignKey(PayrollPeriod,on_delete=models.PROTECT,related_name='payslips')
    basic_salary=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    allowances=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    overtime=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    deductions=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    employer_contribution=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    remarks=models.TextField(blank=True); released_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-period__pay_date','employee__full_name']; unique_together=('employee','period')
    @property
    def gross_pay(self): return self.basic_salary+self.allowances+self.overtime
    @property
    def net_pay(self): return self.gross_pay-self.deductions
    def release(self): self.status=self.Status.RELEASED; self.released_at=timezone.now(); self.save(update_fields=['status','released_at','updated_at'])
