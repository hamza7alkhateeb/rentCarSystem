from rest_framework.routers import DefaultRouter

from .views import VehicleView,VehicleDetailView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('vehicle',VehicleView.as_view(),name='vehicle' ),
    path('vehicle/<int:pk>',VehicleDetailView.as_view(),name='vehicle_details' ),
]