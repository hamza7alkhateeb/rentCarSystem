from django.urls import path
from .views import AuthViewSet

auth_list = AuthViewSet.as_view({
    'post': 'register'
})
auth_login = AuthViewSet.as_view({
    'post': 'login'
})

urlpatterns = [
    path('register/', auth_list, name='register'),
    path('login/', auth_login, name='login'),
]
