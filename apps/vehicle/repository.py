from .models import Vehicle
from django.core.exceptions import ObjectDoesNotExist
from ..booking.models import Booking

class VehicleRepository:
    """
    Repository layer responsible for all Vehicle-related ORM operations.
    Keeps database logic isolated from views to maintain clean architecture.
    """
    def get_all(self,filters=None):
        """
        Get all vehicles with optional filtering.

        Supported filters:
        - vehicle_type (exact match)
        - brand (case-insensitive contains)
        - model (case-insensitive contains)

        Returns:
            QuerySet: Filtered list of vehicles.
        """
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
        """
        Get vehicles available within a given date range.

        A vehicle is unavailable if it has a booking that:
        - Is in status PENDING or CONFIRMED
        - Overlaps the target date range:
            booking.start_date < end_date  AND
            booking.end_date   > start_date

        Args:
            start_date (date): Start of requested period.
            end_date (date): End of requested period.
            filters (dict): Optional vehicle filters.

        Returns:
            QuerySet: Vehicles NOT in conflicting bookings.
        """
        queryset = self.get_all(filters)
        conflicting_bookings = Booking.objects.filter(
            status__in=[Booking.BookingStatus.PENDING, Booking.BookingStatus.CONFIRMED],
            start_date__lt=end_date,
            end_date__gt=start_date
        ).values_list('vehicle_id', flat=True)

        queryset  = queryset.exclude(id__in=conflicting_bookings)
        return queryset

    def get_by_id(self,vehicle_id):
        """
        Retrieve a single Vehicle by ID.

        Returns:
            Vehicle | None: Vehicle if exists, otherwise None.
        """
        try:
            return Vehicle.objects.get(id=vehicle_id)
        except ObjectDoesNotExist:
            return None
    def create(self, **data):
        """
        Create a new Vehicle instance.

        Steps:
        - Build Vehicle object
        - Validate fields using full_clean()
        - Save to database

        Returns:
            Vehicle: The created vehicle object.
        """
        vehicle=Vehicle(**data)
        vehicle.full_clean()
        vehicle.save()
        return vehicle

    def update(self, vehicle, **data):
        """
        Update an existing vehicle.

        Steps:
        - Assign updated fields dynamically
        - Validate using full_clean()
        - Save to database

        Args:
            vehicle (Vehicle): The vehicle instance to update.
            **data: Updated fields.

        Returns:
            Vehicle: Updated vehicle instance.
        """

        for key, value in data.items():
            setattr(vehicle, key, value)
        vehicle.full_clean()
        vehicle.save()
        return vehicle

    def delete(self, vehicle):
        """
        Delete a vehicle instance from the database.

        Args:
            vehicle (Vehicle): The vehicle to delete.
        """
        vehicle.delete()