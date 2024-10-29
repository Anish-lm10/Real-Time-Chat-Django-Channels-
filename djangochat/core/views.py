from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.
def home(request):
    return render(request,'pages/home.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Username not registered!!")
            return redirect('log_in')

        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfully")
            return redirect('rooms')
        else:
            messages.error(request,"Incorrect Password!")
            return redirect('log_in')
    return render(request,'auth/login.html')

def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        cpassword=request.POST.get('confirmpassword')

        if password == cpassword:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,"Username Already Exists!!")
                else:
                    User.objects.create_user(username=username,password=password)
                    messages.success(request,"Account Registered Successfully")
                    return redirect('log_in')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                    return redirect('signup')

        else:
            messages.error(request,"Password must be same!!")
            return redirect('signup')
            
    return render(request,'auth/register.html')

def log_out(request):
    logout(request)
    return redirect('home')

@login_required(login_url='log_in')
def rooms(request):
    rooms=Rooms.objects.all()
    return render(request,'pages/rooms.html',{'rooms':rooms})

@login_required(login_url='log_in')
def room(request,slug):
    room=Rooms.objects.get(slug=slug)
    messages=Messages.objects.filter(room=room)[0:25]
    return render(request,'pages/room.html',{'room':room,'messages':messages})