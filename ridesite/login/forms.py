from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)
    email = forms.EmailField()
    
class UserForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)