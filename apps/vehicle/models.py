from django.db import models
from .enums import VehicleType
class Vehicle(models.Model):
    """
    Represents a vehicle in the rental system.

    Stores essential details such as brand, model, pricing, category, and timestamps.
    Uses Enum-based choices (VehicleType) for `vehicle_type`.
    """
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    vehicle_type = models.CharField(
        max_length=20,
        choices=[(type.value, type.name.title()) for type in VehicleType],
        default=VehicleType.CAR.value,
    )
    daily_rate = models.DecimalField(max_digits=8,decimal_places=2)
    plate_number = models.CharField(max_length=20,unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


