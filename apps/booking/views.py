from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer, VersionOneCreateUserCustomerBookingSerializer, VersionTwoCreateUserCustomerBookingSerializer
from apps.customer.models import Customer


class BookingViewSet(viewsets.ModelViewSet):
    """
    Manage vehicle bookings.

    **List**: View all bookings (filtered by user permissions)
    **Create**: Create new booking with profile completeness check
    **Retrieve**: Get specific booking details
    **Update**: Modify pending booking (customer) or any booking (admin)
    **Delete**: Cancel booking

    **Custom Actions:**
    - `get_booking_by_status`: Filter bookings by status (admin only)
    - `change_status`: Update the status of a booking (admin only)
    - `approve_booking`: Approve a pending booking (admin only)
    - `reject_booking`: Reject a pending booking (admin only)
    """
    queryset = Booking.objects.all().select_related("customer", "vehicle")
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return bookings depending on user role.
        - Admin: all bookings
        - Regular user: only bookings belonging to their customer profile
        """
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all().select_related("customer", "vehicle")
        return Booking.objects.filter(customer__user=user).select_related("vehicle")

    def perform_create(self, serializer):
        """
        Handle booking creation:
        - Admin can specify customer ID
        - Regular users can only create for their own customer profile if profile is complete
        """
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
            missing_fields = customer.get_incomplete_fields()
            if not customer.is_profile_complete():
                raise serializers.ValidationError(
                    {"profile": f"Please complete the following fields before creating a new booking: {', '.join(missing_fields)}."}
                )
            serializer.save(customer=customer)

    @action(detail=False, methods=['get'], url_path="by_status", permission_classes=[permissions.IsAdminUser])
    def get_booking_by_status(self, request):
        """
        Filter bookings by status (admin only).
        Query parameter: `status` (optional)
        """
        status_param = request.query_params.get('status')
        if not status_param:
            all_booking = self.queryset.all()
            serializer = self.get_serializer(all_booking, many=True)
            return Response(serializer.data)
        valid_statuses = [choice[0] for choice in Booking.BookingStatus.choices]
        if status_param not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        bookings = self.queryset.filter(status=status_param)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='change-status', permission_classes=[permissions.IsAdminUser])
    def change_status(self, request, pk=None):
        """
        Change the status of a booking (admin only).
        Request body: `status` (required)
        """
        booking = self.get_object()
        new_status = request.data.get("status")

        valid_statuses = [choice[0] for choice in Booking.BookingStatus.choices]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = new_status
        booking.save()
        return Response(
            {"message": f"Booking status updated to {new_status}"},
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        """
        Update booking:
        - Admin: Can update any booking
        - Customer: Can update only pending bookings
        """
        booking = self.get_object()
        user = self.request.user

        if not user.is_staff:
            if booking.status != Booking.BookingStatus.PENDING:
                raise serializers.ValidationError(
                    {"error": "You can only update bookings that are still pending."}
                )

        serializer.save()

    @action(detail=True, methods=['patch'], url_path='approve', permission_classes=[IsAdminUser])
    def approve_booking(self, request, pk=None):
        """
        Approve a pending booking (admin only)
        """
        booking = self.get_object()
        if booking.status != Booking.BookingStatus.PENDING:
            return Response({"error": "Booking is not pending."}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = Booking.BookingStatus.CONFIRMED
        booking.save()
        return Response({"message": "Booking approved successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='reject', permission_classes=[IsAdminUser])
    def reject_booking(self, request, pk=None):
        """
        Reject a pending booking (admin only)
        """
        booking = self.get_object()
        if booking.status != Booking.BookingStatus.PENDING:
            return Response({"error": "Booking is not pending."}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = Booking.BookingStatus.CANCELLED
        booking.save()
        return Response({"message": "Booking rejected successfully."}, status=status.HTTP_200_OK)


class VersionOneCreateUserCustomerBookingView(APIView):
    """
    Create a new user, customer profile, and booking in a single request (admin only).

    **Request**: User, customer, and booking data
    **Response**: Nested output with user, customer, and booking information
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Handle POST request to create user, customer, and booking.
        Uses transaction.atomic to ensure atomic creation.
        """
        serializer = VersionOneCreateUserCustomerBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            result = serializer.save()

        user = result['user']
        customer = result['customer']
        booking = result['booking']

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        customer_data = {
            "id": customer.id,
            "user_id": customer.user_id,
            "phone_number": customer.phone_number,
            "address": customer.address,
            "driver_license_number": customer.driver_license_number,
            "date_of_birth": customer.date_of_birth
        }
        booking_data = {
            "id": booking.id,
            "customer_id": booking.customer_id,
            "vehicle_id": booking.vehicle_id,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "total_price": booking.total_price,
            "status": booking.status,
            "payment_method": booking.payment_method,
            "notes": booking.notes
        }
        return Response(
            {"user": user_data, "customer": customer_data, "booking": booking_data},
            status=status.HTTP_201_CREATED
        )


class VersionTwoCreateUserCustomerBookingView(APIView):
    """
    Create a booking for an existing user and customer (admin only).

    **Request**: Booking data
    **Response**: Success message
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Handle POST request to create a booking.
        """
        serializer = VersionTwoCreateUserCustomerBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Booking created successfully"}, status=status.HTTP_201_CREATED)
