from apps.booking.models import Booking
from apps.booking.enums import BookingStatus
from datetime import datetime

def get_filtered_bookings(request):
    """
    Returns a filtered queryset of Booking objects based on GET parameters.

    Supports the following filters:
    - start_date: Include bookings starting on or after this date (YYYY-MM-DD).
    - end_date: Include bookings ending on or before this date (YYYY-MM-DD).
    - status: Filter bookings by status (must match BookingStatus enum name).

    Args:
        request (HttpRequest): The incoming request containing GET parameters.

    Returns:
        QuerySet: Filtered and ordered queryset of Booking objects.
    """
    # Start with all bookings, prefetch related customer.user and vehicle for performance

    qs = Booking.objects.select_related('customer__user', 'vehicle').all().order_by('-start_date')

    # Get filters from GET parameters

    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    status_name = request.GET.get('status')

    # Filter by start date if provided
    if start:
        try:
            s = datetime.fromisoformat(start).date()
            qs = qs.filter(start_date__gte=s)
        except:
            pass
    # Filter by end date if provided
    if end:
        try:
            e = datetime.fromisoformat(end).date()
            qs = qs.filter(end_date__lte=e)
        except:
            pass
    # Filter by booking status if provided
    if status_name:
        try:
            status_value = BookingStatus[status_name].value
            qs = qs.filter(status=status_value)
        except KeyError:
            pass
    # Return the final filtered queryset
    return qs
