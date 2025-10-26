from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer
from apps.customer.models import Customer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related("customer", "vehicle")
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all().select_related("customer", "vehicle")
        return Booking.objects.filter(customer__user=user).select_related("vehicle")

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            customer_id = self.request.data.get('customer')
            if not customer_id:
                raise serializers.ValidationError({"customer": "Admin must provide customer id."})
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                raise serializers.ValidationError({"customer": "Customer not found."})
            serializer.save(customer=customer)
        else:
            customer = getattr(user, "customer", None)
            if not customer:
                raise serializers.ValidationError("User does not have a customer profile.")
            serializer.save(customer=customer)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAdminUser])
    def by_status(self, request):
        data = {}
        for status_value, status_label in Booking.BookingStatus.choices:
            bookings = Booking.objects.filter(status=status_value)
            data[status_value] = BookingSerializer(bookings, many=True).data
        return Response(data)

