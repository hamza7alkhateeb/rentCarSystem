from .models import Vehicle
from django.core.exceptions import ObjectDoesNotExist
from ..booking.models import Booking

class VehicleRepository:
    def get_all(self,filters=None):
        queryset=Vehicle.objects.all()
        if filters:
            if 'vehicle_type' in filters:
                queryset = queryset.filter(vehicle_type=filters['vehicle_type'])
            if 'brand' in filters:
                queryset = queryset.filter(brand__icontains=filters['brand'])
            if 'model' in filters:
                queryset = queryset.filter(model__icontains=filters['model'])
        return queryset

    def get_available(self, start_date, end_date, filters=None):
        queryset = self.get_all(filters)
        conflicting_bookings = Booking.objects.filter(
            status__in=[Booking.BookingStatus.PENDING, Booking.BookingStatus.CONFIRMED],
            start_date__lt=end_date,
            end_date__gt=start_date
        ).values_list('vehicle_id', flat=True)

        queryset  = queryset.exclude(id__in=conflicting_bookings)
        return queryset

    def get_by_id(self,vehicle_id):
        try:
            return Vehicle.objects.get(id=vehicle_id)
        except ObjectDoesNotExist:
            return None
    def create(self, **data):
        vehicle=Vehicle(**data)
        vehicle.full_clean()
        vehicle.save()
        return vehicle

    def update(self, vehicle, **data):
        for key, value in data.items():
            setattr(vehicle, key, value)
        vehicle.full_clean()
        vehicle.save()
        return vehicle

    def delete(self, vehicle):
        vehicle.delete()