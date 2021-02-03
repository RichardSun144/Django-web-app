from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class UserForm(forms.Form):
    username = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class DriverForm(forms.Form):
      vehicleType = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
      licenseNumber = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
      containNumber = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
      specialText = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))