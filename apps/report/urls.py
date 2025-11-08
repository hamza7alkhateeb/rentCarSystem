from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path("dashboard/", views.reports_dashboard, name="dashboard"),
    path("bookings/", views.bookings_report_view, name="bookings_report"),
    path("bookings/pdf/", views.bookings_report_pdf, name="bookings_report_pdf"),
    path('vehicle-utilization/', views.vehicle_utilization_report, name='vehicle_utilization'),
    path('vehicle-utilization/pdf/', views.vehicle_utilization_report_pdf, name='vehicle_utilization_pdf'),
]
