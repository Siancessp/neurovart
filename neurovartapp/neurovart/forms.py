from django import forms
from .models import Payouts
from .models import ApplyForFund
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from .models import Customers

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['cus_name', 'cus_mobile']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['profile']

class PasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = Customers
        # fields = ['password']
        fields = [ 'old_password','new_password1', 'new_password2']
class PasswordNewForm(SetPasswordForm):
    class Meta:
        model = Customers
        # fields = ['password']
        fields = [ 'new_password1', 'new_password2']
class RegistrationForm(forms.Form):
    fullname = forms.CharField(label='Your Full Name', max_length=155)
    email = forms.EmailField(label='Your Email')
    mobile = forms.IntegerField(label='Your Mobile')
    sponsor = forms.CharField(label='Sponsor Code')
    password = forms.CharField(label='Your Password')
    confirmPassword = forms.CharField(label='Your Confirm Password')
    country = forms.CharField(label='Your Country Name')
    dialCode = forms.CharField(label='Your dialCode')


class LoginForm(forms.Form):
    email = forms.CharField(label='Your Email', max_length=155)
    password = forms.CharField(label='Your Password')

class ActivationForm(forms.Form):
    amount = forms.FloatField(label='Amount')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Payouts
        fields = [
             'request_amount', 'wallet_address', 'remarks'
        ]


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = ApplyForFund
        fields = [
            'full_name', 'country_code', 'whatsapp_no', 'email',
            'residential_address', 'investment_amount', 'commission_percentage',
            'risk_ratio', 'id_upload', 'performance_link', 'terms'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'country_code': forms.Select(),
            'whatsapp_no': forms.TextInput(attrs={'placeholder': 'Enter your WhatsApp number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'residential_address': forms.TextInput(attrs={'placeholder': 'Enter your residential address'}),
            'investment_amount': forms.NumberInput(attrs={'placeholder': 'Enter your investment amount'}),
            'commission_percentage': forms.NumberInput(attrs={'placeholder': 'Enter your commission percentage'}),
            'risk_ratio': forms.NumberInput(attrs={'placeholder': 'Enter your risk ratio'}),
            'id_upload': forms.ClearableFileInput(),
            'performance_link': forms.URLInput(attrs={'placeholder': 'Enter your performance link'}),
            'terms': forms.CheckboxInput(),
        }