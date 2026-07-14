from django.conf import settings
from django.db import models
class PaymentVoucher(models.Model):
    class Status(models.TextChoices): DRAFT='DRAFT','Draft'; PENDING='PENDING','Pending Approval'; APPROVED='APPROVED','Approved'; PAID='PAID','Paid'; REJECTED='REJECTED','Rejected'
    voucher_no=models.CharField(max_length=40,unique=True)
    payee_name=models.CharField(max_length=180); payee_reference=models.CharField(max_length=100,blank=True)
    purpose=models.TextField(); amount=models.DecimalField(max_digits=14,decimal_places=2)
    payment_method=models.CharField(max_length=40,default='Bank Transfer'); payment_date=models.DateField(null=True,blank=True)
    supporting_object_path=models.CharField(max_length=500,blank=True); receipt_object_path=models.CharField(max_length=500,blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    prepared_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='prepared_vouchers')
    approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='approved_vouchers')
    remarks=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return self.voucher_no
