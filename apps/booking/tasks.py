from celery import shared_task
from django.utils import timezone
from .models import Booking
import logging
from .enums import BookingStatus

logger = logging.getLogger(__name__)

@shared_task
def update_status():

    today = timezone.now().date()

    completed = Booking.objects.filter(
        status=BookingStatus.CONFIRMED.value,
        end_date__lt=today
    )

    count = completed.update(status=BookingStatus.COMPLETED.value)

    logger.info(f"Auto-completed {count} bookings")

    return f"Updated {count} bookings to COMPLETED status"
