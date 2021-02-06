from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, UserForm, DriverForm, RideForm
from .models import UserInfo, DriverInfo, RideInfo
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
'''   
def index(response):
  if response.GET:
    if 'register' in response.GET:
      return redirect('http://vcm-18235.vm.duke.edu:8000/register')
    else:
      return redirect('http://vcm-18235.vm.duke.edu:8000/login')
  return render(response, "login/index.html")
'''

def Driver(response):
    if not response.session.get('is_driver', None):
      return redirect("/http://vcm-18235.vm.duke.edu:8000/driverRegister")
    elif response.GET and 'edit driver profile' in response.GET:
      return redirect("/driverRegister")
    driver_name = response.session['user_name']
    driver = UserInfo.objects.get(username = driver_name)
    driver_info = driver.driverinfo_set.all()
    return render(response, "login/Driver.html", locals())
    
def Passenger(response):
  if response.GET:
    ride_id = response.GET.get('edit_ride')
    to_be_edit_ride = RideInfo.objects.get(id = ride_id)
    ride_form = RideForm()
    return render(response, "login/editRide.html",locals())
    
  ride_list = RideInfo.objects.all()
  return render(response, "login/Passenger.html", locals())

def editRide(response):
  ride_form = RideForm()
  return render(response, "login/editRide.html", locals()) 


def driverRegister(response):
  if response.method == "POST" and response.POST:
    driver_form = DriverForm(data=response.POST)
    if driver_form.is_valid():
      vehicleType = driver_form.cleaned_data["vehicleType"]
      licenseNumber = driver_form.cleaned_data["licenseNumber"]
      containNumber = driver_form.cleaned_data["containNumber"]
      specialText = driver_form.cleaned_data["specialText"]
      username = response.session.get('user_name', None)
      user = UserInfo.objects.get(username = username)
      user.isDriver = True
      user.save()
      response.session['is_driver'] = user.isDriver
      try:
        driver_info = DriverInfo.objects.get(owner = user)
        driver_info.vehicleType = vehicleType
        driver_info.licenseNumber = licenseNumber
        driver_info.containNumber =containNumber
        driver_info.specialText = specialText
      except:
        driver_info = DriverInfo(owner = user, vehicleType=vehicleType, licenseNumber=licenseNumber, containNumber=containNumber, specialText=specialText)   
      driver_info.save()
      return redirect('http://vcm-18235.vm.duke.edu:8000/userPage')
      
  driver_form = DriverForm() 
  driver_name = response.session['user_name']
  driver = UserInfo.objects.get(username = driver_name)
  driver_info_Num = driver.driverinfo_set.count()
  driver_info = driver.driverinfo_set.all()
  return render(response, "login/driverRegister.html", locals()) 
     
def userPage(response):
  if response.GET:
    if 'Passenger' in response.GET:
      return redirect('http://vcm-18235.vm.duke.edu:8000/Passenger')
    else:
      if response.session.get('is_driver', None):
        return redirect('http://vcm-18235.vm.duke.edu:8000/Driver') 
      else:
        return redirect('http://vcm-18235.vm.duke.edu:8000/driverRegister') 
  return render(response, "login/userPage.html")
    

def register(response):
  if response.method == "POST" and response.POST:
    register_form = RegisterForm(data=response.POST)
    if register_form.is_valid():
      username = register_form.cleaned_data["username"]
      password = register_form.cleaned_data["password"]
      email = register_form.cleaned_data["email"]
      try:
        UserInfo.objects.get(username=username)
        message = "User name already exists"
        return render(response, "login/register.html", locals())
      except: 
        UserInfo.objects.create(username=username,password=password,email=email)   
        return redirect('http://vcm-18235.vm.duke.edu:8000/login')
  else:
    register_form = RegisterForm()
  return render(response, "login/register.html", locals()) 



def login(response):
  #if response.session.get('is_login',None):
    #return redirect('/http://vcm-18235.vm.duke.edu:8000/userPage')        
  if response.GET:
    return redirect('/register')    
    
  if response.method == "POST" and response.POST:
    user_form = UserForm(data=response.POST)
    if user_form.is_valid():
      user = user_form.cleaned_data["username"]
      password = user_form.cleaned_data["password"]
      try:
        user = UserInfo.objects.get(username=user)
        if user.password == password:
        #if user.password == password:
          response.session['is_login'] = True
          response.session['user_id'] = user.id
          response.session['user_name'] = user.username
          response.session['user_email'] = user.email
          response.session['is_driver'] = user.isDriver
          return redirect('http://vcm-18235.vm.duke.edu:8000/userPage')
        else:
          message = "wrong password"
      except:
        message = "no user exist"
    #return render(response, 'login/index.html')
    return render(response, 'login/login.html', locals())
  else:
    user_form = UserForm()
  #return render(response, 'login/loginSuccess.html')
  return render(response, 'login/login.html', locals())

def startRide(response):
  if response.method == "POST" and response.POST:
    ride_form = RideForm(data=response.POST)
    if ride_form.is_valid():
      date = ride_form.cleaned_data["date"]
      time = ride_form.cleaned_data["time"]
      startPoint = ride_form.cleaned_data["startPoint"]
      endPoint = ride_form.cleaned_data["endPoint"]
      memberNumber = ride_form.cleaned_data["memberNumber"]
      specialText = ride_form.cleaned_data["specialText"]
      username = response.session.get('user_name', None)
      user = UserInfo.objects.get(username = username)
      '''
      username = response.session.get('user_name', None)
      user = UserInfo.objects.get(username = username)
      user.isDriver = True
      user.save()
      
      try:
        driver_info = DriverInfo.objects.get(owner = user)
        driver_info.vehicleType = vehicleType
        driver_info.licenseNumber = licenseNumber
        driver_info.containNumber =containNumber
        driver_info.specialText = specialText
      except:
        driver_info = DriverInfo(owner = user, vehicleType=vehicleType, licenseNumber=licenseNumber, containNumber=containNumber, specialText=specialText) 
      '''
      ride_info= RideInfo(owner = user, date=date, time=time, startPoint=startPoint, endPoint=endPoint, memberNumber=memberNumber, specialText = specialText) 
      ride_info.save()
      return redirect('http://vcm-18235.vm.duke.edu:8000/Passenger')
  else:
    ride_form = RideForm()
  return render(response, "login/startRide.html", locals()) 
  
  
def logout(response):
  if not response.session.get('is_login', None):
    return redirect("/http://vcm-18235.vm.duke.edu:8000/userPage")
  response.session.flush()
  return redirect('/login')
  


  
'''  
def create(response):
  
  if response.method == "POST":
    form = CreateNewList(response.POST)
    
    if form.is_valid():
      n = form.cleaned_data["question_text"]
      t = Question(question_text=n)
      t.save()
  else:
    form = CreateNewList()
    
  return render(response, 'login/create.html', {}) 
  '''
  
  
'''
  if response.method == "POST":
    form = UserCreationForm(response.POST)
    if form.is_valid():
      form.save()
      return redirect("/registerTrue")
    else:
      form = USerCreationForm()
  form = UserCreationForm()
    '''