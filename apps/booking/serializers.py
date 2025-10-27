from rest_framework import serializers
from apps.booking.models import Booking
from apps.customer.models import Customer
from apps.vehicle.models import Vehicle
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError


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
                raise serializers.ValidationError("This vehicle is not available in the selected period.")
        return data


class CreateUserCustomerBookingSerializer(serializers.Serializer):
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
    payment_method = serializers.ChoiceField(choices=Booking.PaymentMethod.choices)
    notes = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        username = data.get('username')
        driver_licens_number = data.get('driver_licens_number')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        if Customer.objects.filter(driver_licens_number=driver_licens_number).exists():
            raise serializers.ValidationError({"driver_licens_number": "Driver license number already exists."})

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date must be on or after start date."})

        if vehicle and start_date and end_date:
            vehicle_pk = vehicle.pk if hasattr(vehicle, "pk") else int(vehicle)
            is_available = Vehicle.available_in_period(start_date, end_date).filter(pk=vehicle_pk).exists()
            if not is_available:
                raise serializers.ValidationError({"vehicle": "Selected vehicle is not available for the given period."})

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
            customer = Customer.objects.create(user=user, **customer_data)
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
                raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

        return {'user': user, 'customer': customer, 'booking': booking}