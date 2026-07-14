from django import forms
from .models import Notice,Policy
class NoticeForm(forms.ModelForm):
    attachment=forms.FileField(required=False)
    class Meta: model=Notice; fields=('title','content','is_published')
class PolicyForm(forms.ModelForm):
    file=forms.FileField(required=True)
    class Meta: model=Policy; fields=('title','version','is_active')

from .models import Circular
class CircularForm(forms.ModelForm):
    file=forms.FileField(required=True)
    class Meta:
        model=Circular
        fields=['reference_no','title','summary','audience','department','effective_date','expiry_date','is_published']
        widgets={'effective_date':forms.DateInput(attrs={'type':'date'}),'expiry_date':forms.DateInput(attrs={'type':'date'})}
