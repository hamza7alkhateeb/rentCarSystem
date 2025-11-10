import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.vehicle.models import Vehicle


@pytest.fixture
def api_client():
    return APIClient()
@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def user_client(api_client,create_user):
    user= create_user(username="hamza",password="1234")
    response = api_client.post('/api/auth/login/', {"username":"hamza","password":"1234"})
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
@pytest.fixture
def admin_client(api_client,create_user):
    admin = create_user(username="admin",password="1234",is_staff=True)
    response = api_client.post('/api/auth/login/', {"username":"admin","password":"1234"})
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client

@pytest.fixture
def vehicle(db):
    vehicle=Vehicle.objects.create(
        brand="Audi",
        model="A4",
        year=2020,
        vehicle_type="car",
        daily_rate=50.00,
        plate_number="12341234",
        description="Audi car.",
        image=None
    )
    return vehicle

@pytest.fixture
def vehicles(db):
    return [
        Vehicle.objects.create(
        brand="bmw",
        model="M5",
        year=2021,
        vehicle_type="car",
        daily_rate=50.00,
        plate_number="12341234",
        description="bmw car.",
        image=None
    ),
        Vehicle.objects.create(
        brand="bmw",
        model="M8",
        year=2022,
        vehicle_type="car",
        daily_rate=50.00,
        plate_number="00000000",
        description="bmw car.",
        image=None
    )
    ]