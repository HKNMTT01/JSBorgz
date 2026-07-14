from django.contrib import admin
from .models import PaymentVoucher
@admin.register(PaymentVoucher)
class PaymentVoucherAdmin(admin.ModelAdmin): list_display=('voucher_no','payee_name','amount','status','created_at'); list_filter=('status','payment_method')
