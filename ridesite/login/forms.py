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
      
class RideForm(forms.Form):
  date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
  time = forms.TimeField(label = "Time (eg. 14:30)", input_formats=['%H:%M'], widget=forms.TimeInput(format='%H:%M'))
  startPoint = forms.CharField(label = "Start Point", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
  endPoint = forms.CharField(label = "End Point", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
  memberNumber = forms.IntegerField(label = "Member Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
  specialText = forms.CharField(label = "Special Text", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
  isSharable = forms.BooleanField(required=False) 
  
class SearchForm(forms.Form):
  start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
  end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
  start_time = forms.TimeField(label = "Start Time (eg. 14:30)", input_formats=['%H:%M'], widget=forms.TimeInput(format='%H:%M')) 
  end_time = forms.TimeField(label = "End Time (eg. 14:30)", input_formats=['%H:%M'], widget=forms.TimeInput(format='%H:%M')) 
  endPoint = forms.CharField(label = "End Point", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
  memberNumber = forms.IntegerField(label = "Member Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
  
class JoinForm(forms.Form):
  joinNumber = forms.IntegerField(label = "Join Number", min_value = 1, error_messages={"min_value": "At least 1 passenger"}, widget=forms.TextInput(attrs={'class': 'form-control'}))
