from django.db import models
from django.utils import timezone
from rest_framework.serializers import ValidationError
from apps.customer.models import Customer
from apps.vehicle.models import Vehicle

class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        CLIQ = "cliq", "Cliq"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        today = timezone.localdate()
        if self.start_date < today:
            raise ValidationError("Start date cannot be in the past.")
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")

        overlapping = Booking.objects.filter(
            vehicle=self.vehicle,
            status__in=[self.BookingStatus.PENDING, self.BookingStatus.CONFIRMED],
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,

        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This vehicle is not available in the selected period.")

    @property
    def computed_total_price(self):
        if self.start_date and self.end_date and self.vehicle:
            days = (self.end_date - self.start_date).days + 1
            return days * self.vehicle.daily_rate
        return 0

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.computed_total_price
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.user.username} - {self.vehicle} ({self.status})"
