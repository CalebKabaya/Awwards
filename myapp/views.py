from django.shortcuts import render

# Create your views here.

def welcome(request):
    return render(request,'index.html')

def signin(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')
