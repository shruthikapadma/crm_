from django.contrib.auth import logout
from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile


def home(request):
    user_ = None
    user_id = request.session.get('user_id')

    if user_id:
        user_ = UserProfile.objects.filter(id=user_id).first()  # Use .first() to avoid DoesNotExist exception

    return render(request, 'home.html', {
        'user_': user_,
        'request': request
    })






def home(request):
    user_ = None
    user_id = request.session.get('user_id')

    if user_id:
        user_ = UserProfile.objects.filter(id=user_id).first()

    return render(request, 'home.html', {
        'user_': user_,
        'request': request
    })
def register(request):
    return render(request, 'register.html')
def AboutUs(request):
    return render(request, 'AboutUs.html')

def logoutUser(request):
    logout(request)
    return redirect("home")

def ContactUs(request):
    return render(request, 'ContactUs.html')
def services(request):
    return render(request, 'services.html')
def terms(request):
    return render(request, 'terms.html')

def analytics(request):
    return render(request, 'analytics.html')