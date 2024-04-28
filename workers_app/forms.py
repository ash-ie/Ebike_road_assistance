from django import forms

from customer_app.models import *

stat=(('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'))

class MechanicUpdateStatusForm(forms.ModelForm):
    status=forms.ChoiceField(choices=stat,required=True)
    class Meta:
        model = Request
        fields = ['status']


