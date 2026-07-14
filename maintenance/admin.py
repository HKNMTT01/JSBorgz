from django.contrib import admin
from .models import MaintenanceRequest
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin): list_display=('ticket_no','title','priority','status','requested_by','assigned_to'); list_filter=('priority','status','category')
