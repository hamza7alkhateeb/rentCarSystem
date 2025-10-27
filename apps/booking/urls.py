from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, CreateUserCustomerBookingView

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('create-booking/',CreateUserCustomerBookingView.as_view(),name="create-booking"),
]
