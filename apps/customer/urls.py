from django.urls import path
from .views import CustomerViewSet

customer_profile = CustomerViewSet.as_view({'get': 'profile'})
customer_update = CustomerViewSet.as_view({'put': 'update_profile'})

urlpatterns = [
    path('profile/', customer_profile, name='profile'),
    path('profile/update/', customer_update, name='update-profile'),
]
