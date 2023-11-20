from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Re-type Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name','email']
        labels={'first_name':'First name', 'last_name':'Last name', 'email':'Email'}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','required': 'required'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','required': 'required'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }



# class LoginForm(AuthenticationForm):
#     username = UsernameField(widget=forms.TextInput(attrs={
#         'autofocous':True, "class":'form-control'
#     }))
#     password= forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={
#         'class':'form-control', 'autocomplete':'current-password'
#     }))

