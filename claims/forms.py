from django import forms
from .models import Claim
class ClaimForm(forms.ModelForm):
    receipt=forms.FileField(required=False)
    class Meta:
        model=Claim; fields=('title','category','amount','description')
        widgets={'description':forms.Textarea(attrs={'rows':4})}
class ClaimDecisionForm(forms.Form):
    decision=forms.ChoiceField(choices=(('approve','Approve / Forward'),('reject','Reject'))); comment=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':3}))
