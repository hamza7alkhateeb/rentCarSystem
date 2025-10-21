
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from apps.customer.views import CustomerViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet, basename='customer')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer/register/', CustomerViewSet.as_view({'post': 'register'}), name='register'),
    path('customer/login/', CustomerViewSet.as_view({'post': 'login'}), name='login'),
    path('customer/profile/', CustomerViewSet.as_view({'get': 'profile'}), name='profile'),
    path('customer/profile/update/', CustomerViewSet.as_view({'put': 'update_profile'}), name='update-profile'),
]
