from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),  #main page
    #path('create/', views.create, name='create'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('userPage/', views.userPage, name='userPage'),
    path('Passenger/', views.Passenger, name='Passenger'),
    path('Driver/', views.Driver, name='Driver'),
    path('driverRegister/', views.driverRegister, name='driverRegister'),
    path('startRide/', views.startRide, name='startRide'),
]