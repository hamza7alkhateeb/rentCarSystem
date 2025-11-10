from collections import Counter
from calendar import month_name
from datetime import datetime
from apps.booking.models import Booking
from apps.vehicle.models import Vehicle
from apps.booking.enums import BookingStatus
from django.db.models import Sum

def bookings_by_status(bookings_qs):
    """
    Calculates the number of bookings for each status.
    Args:
        bookings_qs (QuerySet): A queryset of Booking objects.
    Returns:
        list: A list of dictionaries with status name and count, e.g.,
              [{"status": "Confirmed", "count": 5}, ...]
    """
    status_counter = Counter([b.status for b in bookings_qs])
    return [
        {"status": status.name.title(), "count": status_counter.get(status.value, 0)}
        for status in BookingStatus
    ]

def calculate_vehicle_utilization(vehicle, month, year, days_in_month):
    """
    Calculates vehicle utilization percentage for a specific month and year.
    Args:
        vehicle (Vehicle): The vehicle object to calculate utilization for.
        month (int): Month number (1-12).
        year (int): Year number (e.g., 2025).
        days_in_month (int): Number of days in the month to calculate percentage.
    Returns:
        dict: A dictionary containing the vehicle, booked days, total days,
              and utilization percentage rounded to 1 decimal.
    """
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
    """
    Calculates total revenue for each month of the given year.
    Args:
        current_year (int): The year for which revenue is calculated.
    Returns:
        list: A list of dictionaries containing month name and total revenue,
              e.g., [{"month": "January", "revenue": 5000}, ...]
    """
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
