from rest_framework import serializers
from .models import Vehicle
from rest_framework.serializers import ValidationError
from datetime import date
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def validate_year(self,value):
        current_year = date.today().year
        if value> current_year:
            raise ValidationError("Year cannot be in the future.")
        return value
    def validate_daily_rate(self, value):
        if value <= 0:
            raise ValidationError("Daily rate must be greater than zero.")
        return value
