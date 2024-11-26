from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Property Management Dashboard!")

def about_us(request):
    return render(request, 'dashboard/about_us.html')

def profile(request):
    return render(request, 'dashboard/profile.html')

def contact_us(request):
    return render(request, 'dashboard/contact_us.html')
