from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        messages.success(request, 'User created successfully')
        return redirect('success')
    else:
        return render(request, 'create_user.html')


def log_reg(request):
    return render(request, 'login_registration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # if request.user.is_authenticated:
        #     return redirect('home')
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('log_reg')
    else:
        return render(request, 'login.html')


def success_view(request):
    return render(request, 'success.html')


@login_required
def home(request):
    return render(request, 'home.html')
