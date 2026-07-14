from django import forms
from .models import PaymentVoucher
class PaymentVoucherForm(forms.ModelForm):
    support_file=forms.FileField(required=False); receipt_file=forms.FileField(required=False)
    class Meta: model=PaymentVoucher; fields=['voucher_no','payee_name','payee_reference','purpose','amount','payment_method','payment_date','status','remarks']; widgets={'payment_date':forms.DateInput(attrs={'type':'date'})}
