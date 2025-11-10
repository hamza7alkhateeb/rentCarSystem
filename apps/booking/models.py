from django.db import models
from apps.customer.models import Customer
from apps.vehicle.models import Vehicle
from apps.booking.enums import BookingStatus, PaymentMethod


class Booking(models.Model):
    """
    Represents a vehicle booking made by a customer.

    Fields:
        customer: FK to the Customer who made the booking.
        vehicle: FK to the Vehicle being booked.
        start_date: Booking start date.
        end_date: Booking end date.
        total_price: Total booking price, auto-calculated if not provided.
        status: Booking status (Pending, Confirmed, Cancelled, Completed).
        payment_method: Payment method (Cash, Cliq).
        notes: Optional booking notes.
        created_at: Timestamp when booking is created.
        updated_at: Timestamp when booking is updated.
    """

    # ----------------------
    # Relationships
    # ----------------------
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='bookings',  # Access all bookings from customer.bookings
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='bookings',  # Access all bookings from vehicle.bookings
    )

    # ----------------------
    # Dates and price
    # ----------------------
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,  # Price can be auto-calculated if left empty
    )

    # ----------------------
    # Status and payment method
    # ----------------------
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name.title()) for status in BookingStatus],
        default=BookingStatus.PENDING.value,  # Default status is pending
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[(method.value, method.name.title()) for method in PaymentMethod],
        default=PaymentMethod.CASH.value,  # Default payment is cash
    )

    # ----------------------
    # Optional notes and timestamps
    # ----------------------
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp when created
    updated_at = models.DateTimeField(auto_now=True)      # Auto timestamp on every update

    # ----------------------
    # Helper methods
    # ----------------------
    @property
    def computed_total_price(self):
        """
        Compute total price based on the vehicle's daily rate
        and the booking duration in days.
        """
        if self.start_date and self.end_date and self.vehicle:
            days = (self.end_date - self.start_date).days + 1  # +1 to include first day
            return days * self.vehicle.daily_rate
        return 0

    def save(self, *args, **kwargs):
        """
        Override save to automatically calculate total_price
        if it hasn't been set manually.
        """
        if not self.total_price:
            self.total_price = self.computed_total_price
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation for admin or debugging:
        Example: "ahmad - Toyota Corolla (pending)"
        """
        return f"{self.customer.user.username} - {self.vehicle} ({self.status})"
