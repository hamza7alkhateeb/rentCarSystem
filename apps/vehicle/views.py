from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, SAFE_METHODS,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import Vehicle
from .serializers import VehicleSerializer
from django.utils import timezone


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class VehicleView(ListCreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Vehicle.objects.all()

        vehicle_type = self.request.query_params.get('vehicle_type')
        brand = self.request.query_params.get('brand')
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        return queryset


class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class AvailableVehiclesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {"error": "start_date and end_date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        today = timezone.now().date()
        if start_date < today or end_date < today:
            return Response(
                {"error": "Dates cannot be in the past."},
                status=status.HTTP_400_BAD_REQUEST
            )

        available_vehicles = Vehicle.available_in_period(start_date, end_date)
        serializer = VehicleSerializer(available_vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)