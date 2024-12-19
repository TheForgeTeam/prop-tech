from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rentals/', views.rentals, name='rentals'),
    path('properties/', views.properties, name='properties'),
]