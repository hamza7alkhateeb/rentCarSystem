from django.db import models

# Create your models here.

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('motorbike', 'Motorbike'),
    ]
    brand = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    vehicle_type = models.CharField(max_length=20,choices=VEHICLE_TYPE_CHOICES)
    daily_rate = models.DecimalField(max_digits=8,decimal_places=2)
    plate_number = models.CharField(max_length=20,unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    id_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"
