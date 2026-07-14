from django.db.models.signals import post_save
from django.dispatch import receiver
from claims.models import Claim
from leave_management.models import LeaveApplication
from maintenance.models import MaintenanceRequest
from payroll.models import Payslip
from vouchers.models import PaymentVoucher
from .models import Notification
from .services import notify

@receiver(post_save,sender=Claim)
def claim_notice(sender,instance,created,**kwargs):
    notify(instance.employee,'Claim submitted' if created else 'Claim status updated',f'{instance.title}: {instance.get_status_display()}',Notification.Type.APPROVAL,f'/claims/')
@receiver(post_save,sender=LeaveApplication)
def leave_notice(sender,instance,created,**kwargs):
    notify(instance.employee,'Leave application submitted' if created else 'Leave status updated',f'{instance.leave_type}: {instance.get_status_display()}',Notification.Type.APPROVAL,'/leave/')
@receiver(post_save,sender=MaintenanceRequest)
def maintenance_notice(sender,instance,created,**kwargs):
    notify(instance.requested_by,'Maintenance ticket created' if created else 'Maintenance ticket updated',f'{instance.ticket_no}: {instance.get_status_display()}',Notification.Type.SYSTEM,f'/maintenance/{instance.pk}/')
@receiver(post_save,sender=Payslip)
def payslip_notice(sender,instance,created,**kwargs):
    if instance.status==Payslip.Status.RELEASED:
        notify(instance.employee,'Payslip released',f'Your {instance.period.name} payslip is available.',Notification.Type.PAYMENT,f'/payroll/{instance.pk}/')
@receiver(post_save,sender=PaymentVoucher)
def voucher_notice(sender,instance,created,**kwargs):
    if instance.prepared_by:
        notify(instance.prepared_by,'Payment voucher created' if created else 'Payment voucher updated',f'{instance.voucher_no}: {instance.get_status_display()}',Notification.Type.PAYMENT,f'/vouchers/{instance.pk}/')
