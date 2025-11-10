from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .repository import CustomerRepo
from .serializers import CustomerSerializer

customer_repo = CustomerRepo()
"""This creates an instance of the Customer repository,
which handles all database interactions for the Customer model"""

class CustomerViewSet(viewsets.ViewSet):
    """ This ViewSet manages customer profile operations (viewing and updating).
     It uses a repository to separate database logic from view logic."""

    permission_classes_by_action = {     # Define permissions for each action (only authenticated users can access)
        'profile': [IsAuthenticated],
        'update_profile': [IsAuthenticated],
    }

    def get_permissions(self):
        """ This method returns the correct permission classes
         depending on the action being executed."""
        permission_classes = self.permission_classes_by_action.get(
            self.action,
            [IsAuthenticated]
        )
        return [permission() for permission in permission_classes]

    def profile(self, request):
        """ This endpoint returns the profile data of the currently logged-in user.
         It fetches the customer object via the repository and serializes it."""
        customer = customer_repo.get_by_user(request.user)
        if not customer:
            return Response({"error": "Customer profile not found"}, status=404)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update_profile(self, request):
        """ This endpoint allows the logged-in user to update their profile.
         It uses the serializer to validate input data before saving changes."""
        customer = customer_repo.get_by_user(request.user)
        if not customer:
            return Response({"error": "Customer profile not found"}, status=404)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the customer data using the repository pattern
            updated_customer = customer_repo.update(customer, serializer.validated_data)
            return Response({
                "message": "Profile updated successfully!",
                "data": CustomerSerializer(updated_customer).data
            })

        # Return validation errors if provided data is invalid
        return Response(serializer.errors, status=400)

