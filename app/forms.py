from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm 
from django.contrib.auth.models import User

from .models import Customer


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus ':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autofocus': 'True'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=' Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label= 'Old Password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-Control'}))
    new_password1 = forms.CharField(label= 'New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-Control'}))
    new_password2 = forms.CharField(label= 'Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-Control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

def __init__(self, *args, **kwargs):
        # Remove the 'user' argument if passed and not needed
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        strip=False
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        strip=False
    )
#class MySetPasswordForm(SetPasswordForm):
#    new_password1 = forms.CharField(
#        label='New Password',
#        widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'})
#    )
#    new_password2 = forms.CharField(
#        label='Confirm New Password',
#        widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'})
#    )

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'from-control'}),
            'locality':forms.TextInput(attrs={'class':'from-control'}),
            'city':forms.TextInput(attrs={'class':'from-control'}),
            'mobile':forms.NumberInput(attrs={'class':'from-control'}),
            'state':forms.Select(attrs={'class':'from-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'from-control'}),
        }