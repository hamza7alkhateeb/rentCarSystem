from django.shortcuts import render
from datetime import datetime
from apps.vehicle.models import Vehicle
from apps.customer.models import Customer
from .utils.filters import get_filtered_bookings
from .utils.calculations import bookings_by_status, calculate_vehicle_utilization, monthly_revenue
from .utils.pdf import render_to_pdf, pdf_response
from django.http import HttpResponse
from django.db.models import Sum
from calendar import month_name
from apps.booking.enums import BookingStatus

# ----------------------------
# Dashboard
# ----------------------------
def reports_dashboard(request):
    """
    Dashboard view that provides a summary of the system:
    - Total bookings
    - Total revenue
    - Bookings by status
    - Total customers
    - Total vehicles
    - Logged-in user's name
    This data is rendered on the dashboard HTML template.
    """
    bookings_qs = get_filtered_bookings(request)
    vehicles_qs = Vehicle.objects.all()
    customers_qs = Customer.objects.all()

    context = {
        "total_bookings": bookings_qs.count(),
        "total_revenue": bookings_qs.aggregate(total=Sum('total_price'))['total'] or 0,
        "by_status": bookings_by_status(bookings_qs),
        "total_customers": customers_qs.count(),
        "total_vehicles": vehicles_qs.count(),
        "user_name": request.user.get_full_name() or request.user.username,
    }
    return render(request, "report/dashboard.html", context)


# ----------------------------
# Bookings Report 
# ----------------------------
def bookings_report_view(request):
    """
    View for displaying a detailed bookings report.
    Includes total bookings, total revenue, bookings by status,
    filter options, and the full list of bookings.
    """
    qs = get_filtered_bookings(request)
    context = {
        "bookings": qs,
        "total_bookings": qs.count(),
        "total_revenue": qs.aggregate(total=Sum('total_price'))['total'] or 0,
        "by_status": bookings_by_status(qs),
        "status_choices": [(status.name, status.value) for status in BookingStatus],
        "filters": {
            "start_date": request.GET.get('start_date', ''),
            "end_date": request.GET.get('end_date', ''),
            "status": request.GET.get('status', ''),
        },
    }
    return render(request, "report/bookings_report.html", context)

def bookings_report_pdf(request):
    """
    Generates a PDF version of the bookings report.
    Uses the same data as bookings_report_view and renders it
    into a PDF file which is returned as an HTTP response.
    """
    qs = get_filtered_bookings(request)
    context = {
        "bookings": qs,
        "total_bookings": qs.count(),
        "total_revenue": qs.aggregate(total=Sum('total_price'))['total'] or 0,
        "by_status": bookings_by_status(qs),
        "generated_at": datetime.now(),
    }
    pdf = render_to_pdf("report/bookings_report_pdf.html", context)
    if pdf:
        return pdf_response(pdf, "bookings_report.pdf")
    return HttpResponse("Error generating PDF", status=500)

# ----------------------------
# Vehicle Utilization Report 
# ----------------------------
def vehicle_utilization_report(request):
    """
    View for displaying vehicle utilization for the current month.
    Calculates how much each vehicle was used and displays the data
    along with the current month and generation timestamp.
    """
    vehicles = Vehicle.objects.all()
    today = datetime.today().date()
    days_in_month = today.day

    data = [calculate_vehicle_utilization(v, today.month, today.year, days_in_month) for v in vehicles]

    context = {
        "vehicles_data": data,
        "month": month_name[today.month],
        "generated_at": datetime.now(),
        
    }
    return render(request, "report/vehicle_utilization_report.html", context)

def vehicle_utilization_report_pdf(request):
    """
    Generates a PDF version of the vehicle utilization report.
    Includes data for each vehicle, month name, timestamp, and
    logged-in user's name.
    """
    vehicles = Vehicle.objects.all()
    today = datetime.today().date()
    days_in_month = today.day

    data = [calculate_vehicle_utilization(v, today.month, today.year, days_in_month) for v in vehicles]

    context = {
        "vehicles_data": data,
        "month": month_name[today.month],
        "generated_at": datetime.now(),
        "user_name": request.user.get_full_name() or request.user.username
    }
    pdf = render_to_pdf("report/vehicle_utilization_report_pdf.html", context)
    if pdf:
        return pdf_response(pdf, f"vehicle_utilization_{today.month}.pdf")
    return HttpResponse("Error generating PDF", status=500)
