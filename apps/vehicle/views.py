from .models import Vehicle
from .serializers import VehicleSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.dateparse import parse_date
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError


class IsAdminOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdminOrIsAuthenticated]

    def get_queryset(self):

        queryset = Vehicle.objects.all()

        vehicle_type = self.request.query_params.get('vehicle_type')
        brand = self.request.query_params.get('brand')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')


        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            today = timezone.now().date()

            if not start_date or not end_date:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

            if start_date < today or end_date < today:
                raise ValidationError("Dates cannot be in the past.")

            if end_date < start_date:
                raise ValidationError("end_date cannot be before start_date.")

            queryset = Vehicle.available_in_period(start_date, end_date)

        if vehicle_type:
            queryset = queryset.filter(vehicle_type__iexact=vehicle_type)

        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        return queryset