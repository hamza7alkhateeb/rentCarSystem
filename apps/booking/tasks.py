from celery import shared_task
from django.utils import timezone
from .models import Booking

@shared_task
def update_status():
    now = timezone.now()
    completed =Booking.objects.filter(
        status=Booking.BookingStatus.CONFIRMED,
        end_date__lt=now
    )

    for booking in completed:
        booking.status = Booking.BookingStatus.COMPLETED
        booking.save()

    return f"Status updated{completed.count()} "

