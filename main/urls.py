from django.urls import path 
from .views import *


urlpatterns = [
    path('',index,name='home'),
    path('like-post/<str:id>',like, name='like'),
    path('comment/<str:id>',comment , name='comment'),
    path('create-post/',create_post , name='create'),
    path('profile/<str:username>',profile,name="profile"),
    path('follow/<str:username>',follow,name="follow"),
    path('delete_post/<str:id>',delete_post,name="delete"),
    path('search/',search,name='search'),
    path('profilesettings/',profilesettings,name='profilesettings'),
]
