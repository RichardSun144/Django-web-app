from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, UserForm, DriverForm, RideForm, SearchForm, JoinForm
from .models import UserInfo, DriverInfo, RideInfo
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.mail import send_mail
# Create your views here.
'''   
def index(request):
  if request.GET:
    if 'register' in request.GET:
      return redirect('http://vcm-18235.vm.duke.edu:8000/register')
    else:
      return redirect('http://vcm-18235.vm.duke.edu:8000/login')
  return render(request, "login/index.html")
'''

def Driver(request):
    if request.GET:
      if 'driver_to_search_ride' in request.GET:
        return redirect("/driverSearchRide")
      if 'confirm_ride' in request.GET:
        ride_id = request.GET.get('confirm_ride')
        ride_to_confirm = RideInfo.objects.get(id = ride_id)
        ride_to_confirm.isConfirmed = True
        ride_to_confirm.driverWho = request.session['user_name']
        ride_to_confirm.save()
        all_open_ride = RideInfo.objects.filter(isConfirmed = False)
        owner = ride_to_confirm.owner
        owner_email = owner.email
        send_mail('Ride Confirm', 'Your ride has been confirmed!', 'bennylee970715@gmail.com', [owner_email])
        sharer_in_ride = ride_to_confirm.sharer.all()
        for sharer in sharer_in_ride:
          sharer_email = sharer.email
          send_mail('Ride Confirm', 'Your ride has been confirmed!', 'bennylee970715@gmail.com', [sharer_email])
        #return render(request, "login/Driver.html", locals())
      if 'complete_ride' in request.GET:
        ride_id = request.GET.get('complete_ride')
        ride_to_complete = RideInfo.objects.get(id = ride_id)
        ride_to_complete.delete()
        #return render(request, "login/Driver.html", locals())
    if not request.session.get('is_driver', None):
      return redirect("/driverRegister")
    elif request.GET and 'edit driver profile' in request.GET:
      return redirect("/driverRegister")
    driver_name = request.session['user_name']
    driver = UserInfo.objects.get(username = driver_name)
    driver_info = driver.driverinfo_set.all()
    driver_info_obj = DriverInfo.objects.get(owner = driver)
    dirver_info_capacity = driver_info_obj.containNumber
    all_open_ride = RideInfo.objects.filter(isConfirmed = False, memberNumber__lte = dirver_info_capacity).exclude(owner = driver)
    all_confirmed_ride = RideInfo.objects.filter(isConfirmed = True, driverWho = request.session['user_name'])
    return render(request, "login/Driver.html", locals())
    
def Passenger(request):
  if request.GET:
    if 'create_ride' in request.GET:
      return redirect("/startRide")
    if 'pas_to_search_ride' in request.GET:
      return redirect("/pasSearchRide")
    if 'join_other_ride' in request.GET:
      #joiner = UserInfo.objects.get(username = request.session['user_name'])
      ride_to_be_joined_id = request.GET.get('join_other_ride')
      request.session['join_other_ride_id'] = ride_to_be_joined_id
      #ride_tobe_joined = RideInfo.objects.get(id = ride_tobe_joined_id)
      #ride_tobe_joined.sharer.add(joiner)
      return redirect("/joinRide")
    ride_id = request.GET.get('edit_ride')
    request.session['edit_ride_id'] = ride_id
    to_be_edit_ride = RideInfo.objects.get(id = ride_id)
    ride_form = RideForm()
    #return render(request, "login/editRide.html",locals())
    return redirect("/editRide")
  user = UserInfo.objects.get(username = request.session['user_name'])
  ride_list_open = RideInfo.objects.filter(isConfirmed = False, owner = user)
  #ride_list_open_owner = RideInfo.objects.filter(isConfirmed = True).filter(owner = user)
  ride_list_open_sharer = user.sharer.all()
  ride_list_open_sharer = ride_list_open_sharer.filter(isConfirmed = False)
  #ride_list_confirmed = RideInfo.objects.filter(isConfirmed = True).filter(Q(owner = user) | Q(sharer = user))
  ride_list_confirmed_owner = RideInfo.objects.filter(isConfirmed = True).filter(owner = user)
  ride_list_confirmed_sharer = user.sharer.all()
  ride_list_confirmed_sharer = ride_list_confirmed_sharer.filter(isConfirmed = True)
  ride_list_other_share = RideInfo.objects.exclude(owner = user).filter(isConfirmed = False, isSharable = True)
  ride_list_other_share = [ride for ride in ride_list_other_share if user not in ride.sharer.all()]
  return render(request, "login/Passenger.html", locals())


def joinRide(request):
  if request.method == "POST" and request.POST:
    join_form = JoinForm(data=request.POST)
    if join_form.is_valid():
      joinNumber = join_form.cleaned_data["joinNumber"]
      join_ride_id = request.session.get('join_other_ride_id', None)
      join_ride = RideInfo.objects.get(id = join_ride_id)
      join_ride.memberNumber = join_ride.memberNumber + joinNumber
      joiner = UserInfo.objects.get(username = request.session['user_name'])
      join_ride.sharer.add(joiner)
      join_ride.save()
    else:
      return render(request, "login/joinRide.html", locals())
    return redirect("/Passenger")
  join_form = JoinForm()
  return render(request, "login/joinRide.html", locals())

  
def editRide(request):
  if request.method == "POST" and request.POST:
    ride_form = RideForm(data=request.POST)
    if ride_form.is_valid():
      date = ride_form.cleaned_data["date"]
      time = ride_form.cleaned_data["time"]
      startPoint = ride_form.cleaned_data["startPoint"]
      endPoint = ride_form.cleaned_data["endPoint"]
      memberNumber = ride_form.cleaned_data["memberNumber"]
      specialText = ride_form.cleaned_data["specialText"]
      #isSharable = ride_form.cleaned_data["isSharable"]
      edit_ride_id = request.session.get('edit_ride_id', None)
      ride_info = RideInfo.objects.get(id = edit_ride_id)
      #ride_info= RideInfo(owner = user, date=date, time=time, startPoint=startPoint, endPoint=endPoint, memberNumber=memberNumber, specialText = specialText) 
      ride_info.date = date
      ride_info.time = time
      ride_info.startPoint = startPoint
      ride_info.endPoint = endPoint
      ride_info.memberNumber = memberNumber
      ride_info.specialText = specialText
      #ride_info.isSharable = isSharable
      ride_info.save()
      return redirect('/Passenger')
  ride_form = RideForm()
  edit_ride_id = request.session.get('edit_ride_id', None)
  to_be_edit_ride = RideInfo.objects.get(id = edit_ride_id)
  return render(request, "login/editRide.html", locals()) 
'''
def search_ride(user, dst, num, sdate, stime, edate, etime):
    querySet = Ride.objects.exclude(owner=user).exclude(driver_id=user.id)
    if dst != "":
        querySet = querySet.filter(destination=dst)
    querySet = querySet.filter(date__gte=sdate).filter(date__lte=edate)
    querySet = querySet.exclude(Q(date=sdate) & Q(time__lte=stime))
    querySet = querySet.exclude(Q(date=edate) & Q(time__gte=etime))
    ride = [r for r in querySet.all() if r.get_left_cap() >= num]
    return ride
'''

def pasSearchRide(request):
  if request.GET:
    if 'pas_search_back' in request.GET:
      return render(request, "login/Passenger.html")
    if 'pas_search_join' in request.GET:
      ride_to_be_joined_id = request.GET.get('pas_search_join')
      request.session['join_other_ride_id'] = ride_to_be_joined_id
      return redirect("/joinRide")
  if request.method == "POST" and request.POST:
    PasSearchRide_form = SearchForm(data=request.POST)
    if PasSearchRide_form.is_valid():
      start_date = PasSearchRide_form.cleaned_data["start_date"]
      end_date = PasSearchRide_form.cleaned_data["end_date"]
      start_time = PasSearchRide_form.cleaned_data["start_time"]
      end_time = PasSearchRide_form.cleaned_data["end_time"]
      endPoint = PasSearchRide_form.cleaned_data["endPoint"]
      memberNumber = PasSearchRide_form.cleaned_data["memberNumber"]
      user = UserInfo.objects.get(username = request.session['user_name'])
      pas_ride_search_result = RideInfo.objects.exclude(owner = user).filter(isConfirmed = False, date__gte=start_date, date__lte=end_date, isSharable = True, memberNumber = memberNumber)
      pas_ride_search_result = pas_ride_search_result.exclude(Q(date=start_date) & Q(time__lte=start_time))
      pas_ride_search_result = pas_ride_search_result.exclude(Q(date=end_date) & Q(time__gte=end_time))    
      return render(request, "login/PasSearchRideResult.html", locals())
  PasSearchRide_form = SearchForm()
  return render(request, "login/PasSearchRide.html", locals()) 


def driverSearchRide(request):
  if request.GET:
    if 'driver_search_back' in request.GET:
      return render(request, "login/Driver.html")
    if 'confirm_search_ride' in request.GET:
      ride_id = request.GET.get('confirm_search_ride')
      ride_to_confirm = RideInfo.objects.get(id = ride_id)
      ride_to_confirm.isConfirmed = True
      ride_to_confirm.driverWho = request.session['user_name']
      ride_to_confirm.save()
      all_open_ride = RideInfo.objects.filter(isConfirmed = False)
      owner = ride_to_confirm.owner
      owner_email = owner.email
      send_mail('Ride Confirm', 'Your ride has been confirmed!', 'bennylee970715@gmail.com', [owner_email])
      sharer_in_ride = ride_to_confirm.sharer.all()
      for sharer in sharer_in_ride:
        sharer_email = sharer.email
        send_mail('Ride Confirm', 'Your ride has been confirmed!', 'bennylee970715@gmail.com', [sharer_email])
      return redirect("/Driver")
  if request.method == "POST" and request.POST:
    DriverSearchRide_form = SearchForm(data=request.POST)
    if DriverSearchRide_form.is_valid():
      start_date = DriverSearchRide_form.cleaned_data["start_date"]
      end_date = DriverSearchRide_form.cleaned_data["end_date"]
      start_time = DriverSearchRide_form.cleaned_data["start_time"]
      end_time = DriverSearchRide_form.cleaned_data["end_time"]
      endPoint = DriverSearchRide_form.cleaned_data["endPoint"]
      memberNumber = DriverSearchRide_form.cleaned_data["memberNumber"]
      user = UserInfo.objects.get(username = request.session['user_name'])
      driver_ride_search_result = RideInfo.objects.exclude(owner = user).filter(isConfirmed = False, date__gte=start_date, date__lte=end_date, memberNumber = memberNumber)
      driver_ride_search_result = driver_ride_search_result.exclude(Q(date=start_date) & Q(time__lte=start_time))
      driver_ride_search_result = driver_ride_search_result.exclude(Q(date=end_date) & Q(time__gte=end_time))    
      return render(request, "login/DriverSearchRideResult.html", locals())
  DriverSearchRide_form = SearchForm()
  return render(request, "login/DriverSearchRide.html", locals()) 

def driverRegister(request):
  if request.method == "POST" and request.POST:
    driver_form = DriverForm(data=request.POST)
    if driver_form.is_valid():
      vehicleType = driver_form.cleaned_data["vehicleType"]
      licenseNumber = driver_form.cleaned_data["licenseNumber"]
      containNumber = driver_form.cleaned_data["containNumber"]
      specialText = driver_form.cleaned_data["specialText"]
      username = request.session.get('user_name', None)
      user = UserInfo.objects.get(username = username)
      user.isDriver = True
      user.save()
      request.session['is_driver'] = user.isDriver
      try:
        driver_info = DriverInfo.objects.get(owner = user)
        driver_info.vehicleType = vehicleType
        driver_info.licenseNumber = licenseNumber
        driver_info.containNumber =containNumber
        driver_info.specialText = specialText
      except:
        driver_info = DriverInfo(owner = user, vehicleType=vehicleType, licenseNumber=licenseNumber, containNumber=containNumber, specialText=specialText)   
      driver_info.save()
      return redirect('/Driver')   
  driver_form = DriverForm() 
  driver_name = request.session['user_name']
  driver = UserInfo.objects.get(username = driver_name)
  driver_info_Num = driver.driverinfo_set.count()
  driver_info = driver.driverinfo_set.all()
  return render(request, "login/driverRegister.html", locals()) 
     
def userPage(request):
  if request.GET:
    if 'Passenger' in request.GET:
      return redirect('/Passenger')
    else:
      if request.session.get('is_driver', None):
        return redirect('/Driver') 
      else:
        return redirect('/driverRegister') 
  return render(request, "login/userPage.html")
    

def register(request):
  if request.method == "POST" and request.POST:
    register_form = RegisterForm(data=request.POST)
    if register_form.is_valid():
      username = register_form.cleaned_data["username"]
      password = register_form.cleaned_data["password"]
      email = register_form.cleaned_data["email"]
      try:
        UserInfo.objects.get(username=username)
        message = "User name already exists"
        return render(request, "login/register.html", locals())
      except: 
        UserInfo.objects.create(username=username,password=password,email=email)   
        return redirect('/login')
  register_form = RegisterForm()
  return render(request, "login/register.html", locals()) 



def login(request):
  #if request.session.get('is_login',None):
    #return redirect('/http://vcm-18235.vm.duke.edu:8000/userPage')        
  if request.GET:
    if 'goToUserPage' in request.GET:
      return redirect('/userPage') 
    return redirect('/register')    
    
  if request.method == "POST" and request.POST:
    user_form = UserForm(data=request.POST)
    if user_form.is_valid():
      user = user_form.cleaned_data["username"]
      password = user_form.cleaned_data["password"]
      try:
        user = UserInfo.objects.get(username=user)
        if user.password == password:
        #if user.password == password:
          request.session['is_login'] = True
          request.session['user_id'] = user.id
          request.session['user_name'] = user.username
          request.session['user_email'] = user.email
          request.session['is_driver'] = user.isDriver
          return redirect('/userPage')
        else:
          message = "wrong password"
      except:
        message = "no user exist"
    #return render(request, 'login/index.html')
    return render(request, 'login/login.html', locals())
  else:
    user_form = UserForm()
  #return render(request, 'login/loginSuccess.html')
  return render(request, 'login/login.html', locals())

def startRide(request):
  if request.method == "POST" and request.POST:
    ride_form = RideForm(data=request.POST)
    if ride_form.is_valid():
      date = ride_form.cleaned_data["date"]
      time = ride_form.cleaned_data["time"]
      startPoint = ride_form.cleaned_data["startPoint"]
      endPoint = ride_form.cleaned_data["endPoint"]
      memberNumber = ride_form.cleaned_data["memberNumber"]
      specialText = ride_form.cleaned_data["specialText"]
      isSharable = ride_form.cleaned_data["isSharable"]
      username = request.session.get('user_name', None)
      user = UserInfo.objects.get(username = username)
      '''
      username = request.session.get('user_name', None)
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
      ride_info= RideInfo(owner = user, date=date, time=time, startPoint=startPoint, endPoint=endPoint, memberNumber=memberNumber, specialText = specialText, isSharable = isSharable) 
      ride_info.save()
      return redirect('/Passenger')
  else:
    ride_form = RideForm()
  return render(request, "login/startRide.html", locals()) 
  
  
def logout(request):
  if not request.session.get('is_login', None):
    return redirect("/userPage")
  request.session.flush()
  return redirect('/login')
  


  
'''  
def create(request):
  
  if request.method == "POST":
    form = CreateNewList(request.POST)
    
    if form.is_valid():
      n = form.cleaned_data["question_text"]
      t = Question(question_text=n)
      t.save()
  else:
    form = CreateNewList()
    
  return render(request, 'login/create.html', {}) 
  '''
  
  
'''
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("/registerTrue")
    else:
      form = USerCreationForm()
  form = UserCreationForm()
    '''