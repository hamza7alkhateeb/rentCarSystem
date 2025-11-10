from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer


class AuthViewSet(viewsets.ViewSet):
    """
    Handle user authentication operations: registration and login.

    **Endpoints:**
        - POST /register/ → Create a new user account
        - POST /login/ → Authenticate existing user and return JWT tokens

    Uses JWT for token-based authentication via `rest_framework_simplejwt`.
    """

    # Permissions can be customized per action (register, login)
    permission_classes_by_action = {
        'register': [AllowAny],  # Allow public registration
        'login': [AllowAny],     # Allow public login
    }

    def get_permissions(self):
        """
        Override the default permission behavior to allow per-action permissions.
        """
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # Default to no special permissions if not specified
            return [permission() for permission in []]

    # --------------------------------------------------------
    # Register Endpoint
    # --------------------------------------------------------
    def register(self, request):
        """
        Handle user registration.

        - Validates input data using RegisterSerializer.
        - Creates a new user if validation passes.
        - Returns success message or validation errors.

        Request body example:
        {
            "username": "ahmad",
            "password": "mypassword123",
            "confirm_password": "mypassword123"
        }

        Response:
            201 Created → {"message": "User registered successfully!"}
            400 Bad Request → Validation errors
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --------------------------------------------------------
    # Login Endpoint
    # --------------------------------------------------------
    def login(self, request):
        """
        Authenticate user and return JWT tokens.

        - Validates credentials using LoginSerializer.
        - Uses Django's built-in `authenticate()` to verify credentials.
        - Returns access and refresh tokens if valid.

        Request body example:
        {
            "username": "ahmad",
            "password": "mypassword123"
        }

        Response:
            200 OK → {"refresh": "...", "access": "..."}
            401 Unauthorized → {"error": "Invalid credentials"}
            400 Bad Request → Validation errors
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                # Generate JWT tokens for the authenticated user
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            # Authentication failed (invalid username/password)
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # Validation failed (e.g., missing fields)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
