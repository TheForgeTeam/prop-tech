from django.shortcuts import render

def dashboard(request):
    return render(request, 'properties/dashboard.html')

def rentals(request):
    return render(request, 'properties/rentals.html')

def properties(request):
    return render(request, 'properties/properties.html')