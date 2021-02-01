from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  #main page
    #path('create/', views.create, name='create'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('userPage', views.userPage, name='userPage')
]