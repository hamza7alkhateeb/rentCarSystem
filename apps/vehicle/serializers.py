from rest_framework import serializers
from .models import Vehicle
from rest_framework.serializers import ValidationError
from datetime import date
class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer responsible for validating and transforming Vehicle model data.
    Used for:
    - Creating vehicles
    - Updating vehicles
    - Listing & retrieving vehicle details
    """
    class Meta:
        model = Vehicle
        fields = '__all__'

    def validate_year(self,value):
        """
        Validate the 'year' field.

        Ensures:
        - Year is not in the future

        Raises:
            ValidationError: If year > current year.
        """
        current_year = date.today().year
        if value> current_year:
            raise ValidationError("Year cannot be in the future.")
        return value
    def validate_daily_rate(self, value):
        """
        Validate the 'daily_rate' field.

        Ensures:
        - Daily rate must be positive and greater than zero

        Raises:
            ValidationError: If rate <= 0.
        """
        if value <= 0:
            raise ValidationError("Daily rate must be greater than zero.")
        return value
