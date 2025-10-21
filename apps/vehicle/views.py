from django.shortcuts import render
from .models import Vehicle
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import VehicleSerializer
from rest_framework.permissions import IsAdminUser

# this for get list item of vehicle and for add new item
class VehicleView(ListCreateAPIView):

    serializer_class = VehicleSerializer
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            queryset = Vehicle.objects.filter(is_available=is_available.lower()=="true")
            return queryset
        queryset = Vehicle.objects.all()
        return queryset
# this for get,update or delete item
class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    # permission_classes = [IsAdminUser]