from django import forms

from customer_app.models import *


class RequestForm(forms.ModelForm):
    class Meta:
        model=Request
        fields=['category','vehicle_no','vehicle_name','vehicle_model','vehicle_brand','location','problem_description']
        widgets = {
        'problem_description':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['message']
        widgets = {
        'message':forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }