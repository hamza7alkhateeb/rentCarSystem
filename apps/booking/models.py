from django.db import models
from apps.customer.models import Customer
from apps.vehicle.models import Vehicle
from enum import Enum
from django.core.exceptions import ValidationError


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class PaymentMethod(str, Enum):
    CASH = "cash"
    CLIQ = "cliq"

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name.title()) for status in BookingStatus],
        default=BookingStatus.PENDING.value
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[(method.value, method.name.title()) for method in PaymentMethod],
        default=PaymentMethod.CASH.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.customer.user.username} - {self.vehicle} ({self.status})"
