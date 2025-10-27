from rest_framework import serializers
from django.contrib.auth.models import User
from apps.customer.models import Customer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        Customer.objects.create(user=user)  
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username','password']
        extra_kwargs = {'password':{'write_only':True}}
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user
