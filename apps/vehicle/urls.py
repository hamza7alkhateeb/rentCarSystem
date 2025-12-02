from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, TestStoreCacheView
from django.urls import path, include



router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='vehicle')



urlpatterns = [
    path('', include(router.urls)),
    path('cache/', TestStoreCacheView.as_view())
]