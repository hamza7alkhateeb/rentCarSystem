from rest_framework import serializers
from .models import Customer
from rest_framework.serializers import ValidationError
import re
import datetime
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['user']

    def validate_phone_number(self, value):
        if not re.match(r'^\d+$', value):
            raise ValidationError("Phone number must contain digits only.")
        if not (9 <= len(value) <= 12):
            raise ValidationError("Phone number must be between 9 and 12 digits.")


        if Customer.objects.filter(phone_number=value).exists():
            raise ValidationError("This phone number is already registered.")
        return value


    def validate_driver_licens_number(self, value):
        if value and len(value) < 6:
            raise ValidationError("Driver license number must be at least 6 characters long.")
        if Customer.objects.filter(driver_licens_number=value).exists():
            raise ValidationError("This driver licens number is already registered.")
        return value


    def validate_date_of_birth(self, value):
        if value:
            today = datetime.date.today()
            if value > today:
                raise ValidationError("Date of birth cannot be in the future.")
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 18:
                raise ValidationError("Customer must be at least 18 years old.")
        return value


    def validate_address(self, value):
        if value and len(value) < 5:
            raise ValidationError("Address is too short.")
        return value

    ####### DON'T Remove ##########################################


    # def validate(self, attrs):
    #     driver_license = attrs.get("driver_licens_number")
    #     license_image = attrs.get("license_image")
    #
    #     if driver_license and not license_image:
    #         raise ValidationError("License image is required when driver license number is provided.")
    #     return attrs

    ####### DON'T Remove ##########################################

    def create(self, validated_data):
        user = validated_data.get("user")

        if Customer.objects.filter(user=user).exists():
            raise ValidationError("This user already has a customer profile.")

        return super().create(validated_data)

