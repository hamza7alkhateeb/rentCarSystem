from rest_framework import status
from .repository import VehicleRepository
from .serializers import VehicleSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.dateparse import parse_date
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)

class IsAdminOrIsAuthenticated(BasePermission):
    """
    Custom permission:
    - Allows authenticated users to perform safe methods (GET, HEAD, OPTIONS)
    - Allows only admin users (is_staff) to perform write operations (POST, PUT, DELETE)
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class VehicleViewSet(ViewSet):
    """
    Vehicle Views

    Provides API endpoints for managing vehicles within the system.
    Built using Django REST Framework with a clean separation via the repository layer.

    **Core Endpoints:**
    - **List**: Retrieve paginated list of vehicles with optional filters (vehicle_type, model, brand)
    - **Retrieve**: Get detailed information about a specific vehicle
    - **Create**: Add new vehicle (admin only)
    - **Update**: Edit existing vehicle data (admin only)
    - **Delete**: Remove a vehicle (admin only, logs deletion action)

    **Custom Actions:**
    - `available`: Check and return all vehicles available within a specified date range
      Requires: `start_date`, `end_date` → Format `YYYY-MM-DD`

    **Permissions:**
    - Authenticated users can view data (safe methods)
    - Only admin users can modify vehicle data (POST/PUT/DELETE)

    **Utilities Used:**
    - Pagination via `PageNumberPagination`
    - Repository layer for database access abstraction
    - Logging for tracking destructive actions
    """

    """
    API endpoints for managing vehicles.
    Uses VehicleRepository for database operations and a clean architecture approach.
    """

    permission_classes = [IsAdminOrIsAuthenticated]
    repository = VehicleRepository()
    pagination_class = PageNumberPagination

    def list(self, request):
        """
        GET /vehicles/
        Returns a paginated list of vehicles.
        Supports filtering by:
        - vehicle_type
        - brand
        - model
        """
        filters={
            key:request.query_params.get(key)
            for key in ['vehicle_type', 'model', 'brand']
            if request.query_params.get(key)
        }
        vehicles = self.repository.get_all(filters)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(vehicles, request)
        serializer = VehicleSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=['get'],url_path='available')
    def available(self,request):
        """
        GET /vehicles/available/
        Returns a list of vehicles available between a given date range.
        Required query params:
        - start_date (YYYY-MM-DD)
        - end_date   (YYYY-MM-DD)

        Validates:
        - Both dates exist
        - Valid date format
        - Dates not in the past
        - end_date is not before start_date
        """
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')

        if not start or not end:
            raise ValidationError("Both start_date and end_date are required. Format: YYYY-MM-DD.")

        start_date = parse_date(start)
        end_date = parse_date(end)

        if not start_date or not end_date:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

        today = timezone.now().date()
        if start_date < today or end_date < today:
            raise ValidationError("Dates cannot be in the past.")

        if end_date < start_date:
            raise ValidationError("end_date cannot be before start_date.")
        filters = {
            key: request.query_params.get(key)
            for key in ['vehicle_type', 'model', 'brand']
            if request.query_params.get(key)
        }
        available = self.repository.get_available(start_date, end_date, filters)
        serializer = VehicleSerializer(available, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
       GET /vehicles/{id}/
       Returns details for a single vehicle.
       If not found -> returns 404.
       """
        vehicle = self.repository.get_by_id(pk)
        if not vehicle:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def create(self, request):
        """
        POST /vehicles/
        Creates a new vehicle.
        Only admin users can access this endpoint.
        """
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            vehicle = self.repository.create(**serializer.validated_data)
            return Response(VehicleSerializer(vehicle).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        PUT /vehicles/{id}/
        Updates an existing vehicle.
        Only admin users can perform updates.
        Returns 404 if vehicle is not found.
        """
        vehicle = self.repository.get_by_id(pk)
        if not vehicle:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            updated_vehicle = self.repository.update(vehicle, **serializer.validated_data)
            return Response(VehicleSerializer(updated_vehicle).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        DELETE /vehicles/{id}/
        Deletes an existing vehicle.
        Logs deletion information including plate number and the user who deleted it.
        Only admin users can delete.
        """
        vehicle = self.repository.get_by_id(pk)
        if not vehicle:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
        logger.warning(
            f"Vehicle with plate number-{vehicle.plate_number} deleted by {request.user.username}"
        )
        self.repository.delete(vehicle)
        return Response(status=status.HTTP_204_NO_CONTENT)