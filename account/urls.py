from django.urls import path 
from .views import *


urlpatterns = [
    path('settings/',settings,name="settings"),
    path('signin/',signin,name="signin"),
    path('signup/',signup,name="signup"),
    path('myprofile/',myprofile,name="myprofile"),
    path('logout/',logout, name='logout'),
    path('confirm/<str:id>',confirm , name='confirm')
]