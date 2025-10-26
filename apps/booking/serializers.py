from rest_framework import serializers
from apps.booking.models import Booking

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
