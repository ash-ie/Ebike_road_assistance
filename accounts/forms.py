import re
from django import forms
from accounts.models import *
from customer_app.models import *
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email','password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already in use')
        return username
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')
    
class CustomerRegistrationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    mobile_number = forms.CharField(required=True,validators=[phone_number_validator])
    class Meta:
        model = UserProfile
        fields = ['name', 'mobile_number']

class WorkerRegistrationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    mobile_number = forms.CharField(required=True,validators=[phone_number_validator])
    profile_pic = forms.ImageField(required=True)
    class Meta:
        model = UserProfile
        fields = ['name', 'mobile_number','profile_pic']

stat=(('Pending','Pending'),('Approved','Approved'),('Released','Released'))

class AdminApproveRequestForm(forms.ModelForm):
    cost = forms.IntegerField(required=True)
    status=forms.ChoiceField(choices=stat,required=True)
    class Meta:
        model = Request 
        fields = ['mechanic', 'cost', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mechanic'].queryset = User.objects.filter(role=2)
