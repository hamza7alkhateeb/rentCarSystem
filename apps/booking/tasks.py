from celery import shared_task
from django.utils import timezone
from .models import Booking
import logging
from .enums import BookingStatus
from datetime import timedelta
# Initialize a logger for this module
logger = logging.getLogger(__name__)


@shared_task
def update_status():
    """
    Celery task to automatically update the status of bookings.

    Workflow:
    1. Get current date.
    2. Filter bookings that are CONFIRMED but have ended (end_date < today).
    3. Bulk update their status to COMPLETED.
    4. Log the number of bookings updated.
    
    Returns:
        str: Message with count of updated bookings.
    """
    today = timezone.now().date()  # Current date without time

    # Filter bookings that are CONFIRMED and have already ended
    completed = Booking.objects.filter(
        status=BookingStatus.CONFIRMED.value,  # Use Enum value for DB field
        end_date__lt=today
    )

    # Bulk update status for efficiency
    count = completed.update(status=BookingStatus.COMPLETED.value)

    # Log info for monitoring
    logger.info(f"Auto-completed {count} bookings")

    return f"Updated {count} bookings to COMPLETED status"



@shared_task
def auto_cancel_booking_expired():
    expired_time=timezone.now() - timedelta(hours=24)
    expired_bookings = Booking.objects.filter(status=BookingStatus.PENDING.value,created_at__lt=expired_time)
    count = expired_bookings.count()
    expired_bookings.update(status=BookingStatus.CANCELLED.value)

    return f"Updated {count} bookings to CANCELLED status"