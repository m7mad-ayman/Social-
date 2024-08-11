from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from .models import *
from main.models import Post
import datetime ,re 
# Create your views here.
def signin(request):
    if request.method =="POST":
        if not (request.POST["username"] == '') or not (request.POST["password"]=='') :
            if "@" in request.POST['username']:
                username = request.POST["username"]
                password = request.POST["password"]
                user=auth.authenticate(email = request.POST['username'],password=request.POST['password'])
            else:
                username = request.POST["username"]
                password = request.POST["password"] 
                user=auth.authenticate(username = username,password=password)
            if user != None:
                auth.login(request,user)
                
                return redirect("/")
            else:
                return render(request,"signin.html",{"message":"username or password isn't correct"})
        else:
           return render(request,"signin.html",{"message":"username or password can't be empty"})
    
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,"signin.html")

@csrf_protect
def confirm(request,id):
    confirm = Confirm.objects.get(id=id)
    if request.method == "POST":
        if request.POST['code']=='':
            if request.POST["code"]==confirm.code:
                User=auth.get_user_model()
                user=User(username=confirm.username,email=confirm.email)
                user.set_password(confirm.password)  
                user.save()  
                Profile(user=user).save()
                user=auth.authenticate(username = confirm.username,password=confirm.password)            
                confirm.delete()
                if user != None:
                    auth.login(request,user)
                    return redirect("/settings/")
                else:print('user is none')
            else:
                return render(request,'confirm.html',{'email':confirm.email,"id":id,"message":"code isn't correct"})
        else:
                return render(request,'confirm.html',{'email':confirm.email,"id":id,"message":"write your code"})
    elif request.method == "GET":
        
        return render(request,'confirm.html',{'email':confirm.email,"id":id})

        
@csrf_protect
def signup(request):
    if request.method=="POST":
        if request.POST.get('agree') == "on":
            User = get_user_model()
            if not (request.POST["username"] == '') or not (request.POST["email"]=='') or not (request.POST["password"]=='') or not (request.POST["confirm"]=='') :
                if not User.objects.filter(username = request.POST.get('username')).exists() and not User.objects.filter(email = request.POST.get('email')).exists(): 
                    if not ('@' in request.POST.get('username')) or not (' ' in request.POST.get('username')):
                        if "@" in str(request.POST.get('email')): 
                            
                            if request.POST.get('password') == request.POST.get('confirm'):
                                if len(request.POST.get('password'))>=8 and (not str(request.POST.get('password')).isalpha()) and not(str(request.POST.get('password')).isnumeric()) :
                                    if not Confirm.objects.filter(email=request.POST['email']).exists():
                                        password = make_password(request.POST['password'])
                                        confirm=Confirm(username=request.POST['username'],email=request.POST['email'],password=password,code = get_random_string(length=5),expire = datetime.datetime.now()+datetime.timedelta(minutes=2))
                                        confirm.save()

                                        send_mail("Email Confirmation",
                                        "your confirmation code : {0}".format(confirm.code),
                                        "Django E-Commerce",
                                        [confirm.email])
                                        print('[ Django Server ] : Email Sent to ({0})'.format(request.POST["email"]))
                                        return redirect('/confirm/'+str(confirm.id))
                                    else:
                                        confirm = Confirm.objects.get(email=request.POST['email'])
                                        return redirect('/confirm/'+str(confirm.id))
                                else:
                                    return render(request,"signup.html",{"message":"password must contain letters and numbers , 8 at least"})
                            else:
                                return render(request,"signup.html",{"message":"passwords don't match"})
                        else:
                            return render(request,"signup.html",{"message":"email isn't valid"})
                    else:
                        return render(request,"signup.html",{"message":"not valid username"})    
                    
                else:
                    return render(request,"signup.html",{"message":"username or email is already taken"})
            else:
                return render(request,"signup.html",{'message':"Don't leave any field empty"})
        else: 
            return render(request,"signup.html",{"message":"You must agree the terms"}) 
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,"signup.html")
   
      


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect("/signin/")



   
@login_required(login_url='signin')
def settings(request):
    return render(request,"settings.html")

@login_required(login_url='signin')
def myprofile(request):
    User = get_user_model()
    user=User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(profile=profile)
    
    return render(request,"myprofile.html",{"myprofile":profile,"username":request.user.username,"posts":posts})
