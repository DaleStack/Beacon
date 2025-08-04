from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def custom_logout(request):
    logout(request)
    return redirect('/')
