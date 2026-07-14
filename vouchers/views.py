from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,redirect,render
from accounts.models import User
from core.storage import upload_private,signed_url
from .forms import PaymentVoucherForm
from .models import PaymentVoucher

def allowed(u): return u.is_superuser or u.role in {User.Role.ADMIN,User.Role.GM_HR,User.Role.GM_FINANCE,User.Role.CEO}
@login_required
def voucher_list(request):
    if not allowed(request.user): raise PermissionDenied
    return render(request,'vouchers/list.html',{'vouchers':PaymentVoucher.objects.select_related('prepared_by','approved_by')})
@login_required
def voucher_create(request):
    if not allowed(request.user): raise PermissionDenied
    form=PaymentVoucherForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.prepared_by=request.user
        if form.cleaned_data.get('support_file'): obj.supporting_object_path=upload_private(form.cleaned_data['support_file'],'payment-vouchers/support')
        if form.cleaned_data.get('receipt_file'): obj.receipt_object_path=upload_private(form.cleaned_data['receipt_file'],'payment-vouchers/receipts')
        obj.save(); messages.success(request,'Payment voucher saved.'); return redirect('voucher_list')
    return render(request,'shared/form_page.html',{'form':form,'title':'New payment voucher','subtitle':'Record payee, amount and supporting documents.'})
@login_required
def voucher_detail(request,pk):
    if not allowed(request.user): raise PermissionDenied
    return render(request,'vouchers/detail.html',{'voucher':get_object_or_404(PaymentVoucher,pk=pk)})
@login_required
def voucher_action(request,pk,action):
    if not allowed(request.user): raise PermissionDenied
    obj=get_object_or_404(PaymentVoucher,pk=pk)
    if request.method=='POST':
        mapping={'submit':obj.Status.PENDING,'approve':obj.Status.APPROVED,'paid':obj.Status.PAID,'reject':obj.Status.REJECTED}
        if action in mapping: obj.status=mapping[action]; obj.approved_by=request.user if action=='approve' else obj.approved_by; obj.save(); messages.success(request,'Voucher status updated.')
    return redirect('voucher_detail',pk=pk)
@login_required
def voucher_file(request,pk,kind):
    if not allowed(request.user): raise PermissionDenied
    obj=get_object_or_404(PaymentVoucher,pk=pk); path=obj.receipt_object_path if kind=='receipt' else obj.supporting_object_path
    if not path: messages.error(request,'No document uploaded.'); return redirect('voucher_detail',pk=pk)
    return redirect(signed_url(path))
