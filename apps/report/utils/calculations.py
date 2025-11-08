from collections import Counter
from calendar import month_name
from datetime import datetime
from apps.booking.models import Booking
from apps.vehicle.models import Vehicle
from apps.booking.enums import BookingStatus
from django.db.models import Sum

def bookings_by_status(bookings_qs):
    status_counter = Counter([b.status for b in bookings_qs])
    return [
        {"status": status.name.title(), "count": status_counter.get(status.value, 0)}
        for status in BookingStatus
    ]

def calculate_vehicle_utilization(vehicle, month, year, days_in_month):
    bookings = Booking.objects.filter(
        vehicle=vehicle,
        start_date__month=month,
        start_date__year=year,
    )
    total_bookings_days = sum([(b.end_date - b.start_date).days + 1 for b in bookings], 0)
    utilization = (total_bookings_days / days_in_month) * 100 if days_in_month > 0 else 0
    return {
        "vehicle": vehicle,
        "booked_days": total_bookings_days,
        "total_days": days_in_month,
        "utilization": round(utilization, 1),
    }

def monthly_revenue(current_year):
    monthly_data = []
    for month in range(1, 13):
        total = Booking.objects.filter(
            start_date__year=current_year,
            start_date__month=month
        ).aggregate(total=Sum('total_price'))['total'] or 0

        monthly_data.append({
            "month": month_name[month],
            "revenue": total,
        })
    return monthly_data
