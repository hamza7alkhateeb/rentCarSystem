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
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class VehicleViewSet(ViewSet):
    permission_classes = [IsAdminOrIsAuthenticated]
    repository = VehicleRepository()
    pagination_class = PageNumberPagination

    def list(self, request):
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
        vehicle = self.repository.get_by_id(pk)
        if not vehicle:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def create(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            vehicle = self.repository.create(**serializer.validated_data)
            return Response(VehicleSerializer(vehicle).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        vehicle = self.repository.get_by_id(pk)
        if not vehicle:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            updated_vehicle = self.repository.update(vehicle, **serializer.validated_data)
            return Response(VehicleSerializer(updated_vehicle).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        vehicle = self.repository.get_by_id(pk)
        if not vehicle:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
        logger.warning(
            f"Vehicle with plate number-{vehicle.plate_number} deleted by {request.user.username}"
        )
        self.repository.delete(vehicle)
        return Response(status=status.HTTP_204_NO_CONTENT)