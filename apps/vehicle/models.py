from django.db import models
from rest_framework.serializers import ValidationError
from datetime import date

class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        CAR = 'car', 'Car'
        VAN = 'van', 'Van'
        TRUCK = 'truck', 'Truck'
        MOTORBIKE = 'motorbike', 'Motorbike'

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    vehicle_type = models.CharField(max_length=20,choices=VehicleType.choices, default=VehicleType.CAR)
    daily_rate = models.DecimalField(max_digits=8,decimal_places=2)
    plate_number = models.CharField(max_length=20,unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        current_year = date.today().year
        if self.year > current_year:
            raise ValidationError("Year cannot be in the future.")

        if self.daily_rate <= 0 :
            raise ValidationError("Daily rate must be greater than zero.")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


