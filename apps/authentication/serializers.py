from rest_framework import serializers
from django.contrib.auth.models import User
from apps.customer.models import Customer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Create User Serializer
# Reusable in nested serializers
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username','password']
        extra_kwargs = {'password':{'write_only':True}}

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

# API Register Serializer
class RegisterSerializer(CreateUserSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta(CreateUserSerializer.Meta):
        fields = ['username', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super().create(validated_data)