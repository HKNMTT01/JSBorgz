from django import forms
from .models import MaintenanceRequest
class MaintenanceRequestForm(forms.ModelForm):
    attachment=forms.FileField(required=False)
    class Meta: model=MaintenanceRequest; fields=['ticket_no','title','category','location','description','priority','attachment']
class MaintenanceUpdateForm(forms.ModelForm):
    class Meta: model=MaintenanceRequest; fields=['assigned_to','status','priority','resolution_notes']
