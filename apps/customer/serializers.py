from rest_framework import serializers
from .models import Customer
from rest_framework.serializers import ValidationError
import re
import datetime
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        """This serializer converts Customer model data into JSON format (and vice versa)
        It also validates input data to make sure it's correct before saving to the database."""
        model = Customer
        fields = '__all__'
        read_only_fields = ['user']

    def validate_phone_number(self, value):
        """  Validates the phone number field.
             Ensures it contains digits only, has a valid length (9–12),
             and is not already registered in the database."""
        if not re.match(r'^\d+$', value):
            raise ValidationError("Phone number must contain digits only.")
        if not (9 <= len(value) <= 12):
            raise ValidationError("Phone number must be between 9 and 12 digits.")
        qs=Customer.objects.filter(phone_number=value)
        if self.instance:
            qs=qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This phone number is already registered.")
        return value


    def validate_driver_license_number(self, value):
        """ Validates the driver's license number.
            Checks that it's not too short and not already used by another customer."""
        if value and len(value) < 6:
            raise ValidationError("Driver license number must be at least 6 characters long.")
        qs = Customer.objects.filter(driver_license_number=value)
        if self.instance:
            qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This driver license number is already registered.")
        return value


    def validate_date_of_birth(self, value):
        """ Validates the date of birth.
            Ensures the date isn't in the future and that the customer is at least 18 years old."""
        if value:
            today = datetime.date.today()
            if value > today:
                raise ValidationError("Date of birth cannot be in the future.")
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise ValidationError("Customer must be at least 18 years old.")
        return value


    def validate_address(self, value):
        """ Validates the address field.
             Checks that it’s not too short if provided """
        if value and len(value) < 5:
            raise ValidationError("Address is too short.")
        return value


    def validate(self, attrs):

        """Performs cross-field validation
           Ensures that if a driver license number is given, a license image must also be provided"""
        driver_license = attrs.get("driver_license_number")
        license_image = attrs.get("license_image")

        if driver_license and not license_image:
            raise ValidationError("License image is required when driver license number is provided.")
        return attrs



    def create(self, validated_data):
        """ Custom create method
            Prevents creating multiple customer profiles for the same user"""
        user = validated_data.get("user")

        if Customer.objects.filter(user=user).exists():
            raise ValidationError("This user already has a customer profile.")

        return super().create(validated_data)

