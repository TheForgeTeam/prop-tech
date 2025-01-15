from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rentals/', views.rentals, name='rentals'),
    path('properties/', views.properties, name='properties'),
    path('rentals/create/', views.create_rental, name='create_rental'),
    path('properties/create/', views.create_sale, name='create_sale'),
]