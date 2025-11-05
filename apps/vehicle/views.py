from rest_framework import status
from .repositories import VehicleRepository
from .serializers import VehicleSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.dateparse import parse_date
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

class IsAdminOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class VehicleViewSet(ViewSet):
    permission_classes = [IsAdminOrIsAuthenticated]
    repository = VehicleRepository()

    def list(self, request):
        filters={
            key:request.query_params.get(key)
            for key in ['vehicle_type', 'model', 'brand']
            if request.query_params.get(key)
        }
        vehicles = self.repository.get_all(filters)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'],url_path='available')
    def available(self,request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            raise ValidationError("Both start_date and end_date are required. Format: YYYY-MM-DD.")
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
        self.repository.delete(vehicle)
        return Response(status=status.HTTP_204_NO_CONTENT)