from rest_framework import serializers
from django.contrib.auth.models import User
from apps.customer.models import Customer


class LoginSerializer(serializers.Serializer):
    """
    Handle user authentication input.

    Fields:
        - username (CharField): Username for login.
        - password (CharField): User password (write-only).

    Used for validating login credentials before authentication.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# -------------------------------------------------------------------
# Create User Serializer
# -------------------------------------------------------------------
class CreateUserSerializer(serializers.ModelSerializer):
    """
    Base serializer for creating new users.

    Provides:
        - Username uniqueness validation
        - Secure password creation via `create_user`
    
    Can be reused in other serializers (e.g., RegisterSerializer).
    """
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password from responses

    def validate_username(self, value):
        """
        Ensure the username is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        """
        Create a new user with hashed password using Django's create_user().
        """
        return User.objects.create_user(**validated_data)


# -------------------------------------------------------------------
# Register Serializer
# -------------------------------------------------------------------
class RegisterSerializer(CreateUserSerializer):
    """
    Handle user registration.

    Inherits from CreateUserSerializer and adds:
        - confirm_password field for verification.
        - Password match validation before creating a user.

    Example:
        {
            "username": "john_doe",
            "password": "mypassword123",
            "confirm_password": "mypassword123"
        }
    """
    confirm_password = serializers.CharField(write_only=True)

    class Meta(CreateUserSerializer.Meta):
        fields = ['username', 'password', 'confirm_password']

    def validate(self, data):
        """
        Ensure that password and confirm_password match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )
        return data

    def create(self, validated_data):
        """
        Remove confirm_password before creating the user.
        """
        validated_data.pop('confirm_password')
        return super().create(validated_data)
