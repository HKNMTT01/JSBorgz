from django import forms
from .models import LeaveApplication
class LeaveApplicationForm(forms.ModelForm):
    support_document=forms.FileField(required=False)
    class Meta:
        model=LeaveApplication; fields=('leave_type','start_date','end_date','reason','contact_address','contact_phone','recommender','approver')
        widgets={'start_date':forms.DateInput(attrs={'type':'date'}),'end_date':forms.DateInput(attrs={'type':'date'}),'reason':forms.Textarea(attrs={'rows':4}),'contact_address':forms.Textarea(attrs={'rows':2})}
class DecisionForm(forms.Form):
    decision=forms.ChoiceField(choices=(('approve','Approve'),('reject','Reject'))); comment=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':3}))
