from apps.booking.models import Booking
from apps.booking.enums import BookingStatus
from datetime import datetime

def get_filtered_bookings(request):
    qs = Booking.objects.select_related('customer__user', 'vehicle').all().order_by('-start_date')
    
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    status_name = request.GET.get('status')

    if start:
        try:
            s = datetime.fromisoformat(start).date()
            qs = qs.filter(start_date__gte=s)
        except:
            pass

    if end:
        try:
            e = datetime.fromisoformat(end).date()
            qs = qs.filter(end_date__lte=e)
        except:
            pass

    if status_name:
        try:
            status_value = BookingStatus[status_name].value
            qs = qs.filter(status=status_value)
        except KeyError:
            pass

    return qs
