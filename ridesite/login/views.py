from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, UserForm
from .models import UserInfo
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

def userPage(response):
  return render(response, "login/userPage.html")
    

def register(response):
  if response.method == "POST" and response.POST:
    register_form = RegisterForm(data=response.POST)
    if register_form.is_valid():
      username = register_form.cleaned_data["username"]
      password = register_form.cleaned_data["password"]
      email = register_form.cleaned_data["email"]
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