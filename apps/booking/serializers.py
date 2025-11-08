from rest_framework import serializers
from apps.booking.models import Booking,PaymentMethod
from apps.customer.models import Customer
from apps.vehicle.models import Vehicle
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.serializers import ValidationError
from apps.authentication.serializers import UserSerializer
from apps.customer.serializers import CustomerSerializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ['total_price', 'created_at', 'updated_at', 'status','customer']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')
        instance = getattr(self, 'instance', None)

        if start_date and end_date and vehicle:
            overlapping = Booking.objects.filter(
                vehicle=vehicle,
                status__in=[Booking.BookingStatus.PENDING.value, Booking.BookingStatus.CONFIRMED.value],
                start_date__lte=end_date,
                end_date__gte=start_date
            )
            if instance:
                overlapping = overlapping.exclude(pk=instance.pk)
            if overlapping.exists():
                raise ValidationError({"error": "This vehicle is not available in the selected period."})
        return data


class VersionOneCreateUserCustomerBookingSerializer(serializers.Serializer):
    # User fields
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    # Customer fields
    phone_number = serializers.CharField(max_length=12)
    address = serializers.CharField(max_length=300, allow_blank=True, required=False)
    driver_licens_number = serializers.CharField(max_length=20)
    date_of_birth = serializers.DateField(required=False)

    # Booking fields
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    payment_method = serializers.ChoiceField(choices=[(method.value, method.name.title()) for method in PaymentMethod])
    notes = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        username = data.get('username')
        driver_licens_number = data.get('driver_licens_number')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')

        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": "Username already exists."})

        if Customer.objects.filter(driver_licens_number=driver_licens_number).exists():
            raise ValidationError({"driver_licens_number": "Driver license number already exists."})

        if start_date and end_date and end_date < start_date:
            raise ValidationError({"end_date": "End date must be on or after start date."})
        if vehicle and start_date and end_date:
            vehicle_id = vehicle.pk if isinstance(vehicle, Vehicle) else int(vehicle)
            is_conflicting = Booking.objects.filter(
                vehicle_id=vehicle_id,
                status__in=[Booking.BookingStatus.PENDING, Booking.BookingStatus.CONFIRMED],
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()

            if is_conflicting:
                raise ValidationError({"vehicle": "Selected vehicle is not available for the given period."})

        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        customer_data = {
            'phone_number': validated_data.pop('phone_number'),
            'address': validated_data.pop('address', ''),
            'driver_licens_number': validated_data.pop('driver_licens_number'),
            'date_of_birth': validated_data.pop('date_of_birth', None),
        }

        vehicle = validated_data.pop('vehicle')
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)

            customer= Customer.objects.get(user=user)
            for field, value in customer_data.items():
                setattr(customer, field, value)
            customer.save()


            booking = Booking(
                customer=customer,
                vehicle=vehicle,
                start_date=start_date,
                end_date=end_date,
                payment_method=validated_data.get('payment_method', Booking.PaymentMethod.CASH),
                notes=validated_data.get('notes', '')
            )
            try:
                booking.save()
            except ValidationError as e:
                raise ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

        return {'user': user, 'customer': customer, 'booking': booking}



class VersionTwoCreateUserCustomerBookingSerializer(serializers.Serializer):
    user= UserSerializer()
    customer = CustomerSerializer()
    booking = BookingSerializer()

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            customer_data = validated_data.pop("customer")

            customer = Customer.objects.get(user=user)

            for field, value in customer_data.items():
                setattr(customer, field, value)
            customer.save()

            booking_data = validated_data.pop("booking")

            if isinstance(booking_data.get("vehicle"), Vehicle):
                booking_data["vehicle"] = booking_data["vehicle"].id

            booking_serializer = BookingSerializer(data=booking_data)
            booking_serializer.is_valid(raise_exception=True)
            booking = booking_serializer.save(customer=customer)

        return {
            "user": user,
            "customer": customer,
            "booking": booking
        }