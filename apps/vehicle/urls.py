from django.urls import path
from .views import VehicleView, VehicleDetailView, AvailableVehiclesAPIView

urlpatterns = [
    
    path('', VehicleView.as_view(), name='vehicle-list-create'),
    path('available/', AvailableVehiclesAPIView.as_view(), name='available-vehicles'),
    path('<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    
]
