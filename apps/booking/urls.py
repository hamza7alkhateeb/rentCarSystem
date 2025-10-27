from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, VersionOneCreateUserCustomerBookingView,VersionTwoCreateUserCustomerBookingView

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('create-booking-v1/',VersionOneCreateUserCustomerBookingView.as_view(),name="create-booking-v1"),
    path('create-booking-v2/',VersionTwoCreateUserCustomerBookingView.as_view(),name="create-booking-v2"),
]
