
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer

class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('username','email','password')

    def create(self, validated_data):
        user =User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Customer.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'address', 'license_image', 'driver_licens_number', 'date_of_birth',]

