from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .repository import CustomerRepo
from .serializers import CustomerSerializer

customer_repo = CustomerRepo()

class CustomerViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'profile': [IsAuthenticated],
        'update_profile': [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return []

    def profile(self, request):
        customer = customer_repo.get_by_user(request.user)
        if not customer:
            return Response({"error": "Customer profile not found"}, status=404)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update_profile(self, request):
        customer = customer_repo.get_by_user(request.user)
        if not customer:
            return Response({"error": "Customer profile not found"}, status=404)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            updated_customer = customer_repo.update(customer, serializer.validated_data)
            return Response({
                "message": "Profile updated successfully!",
                "data": CustomerSerializer(updated_customer).data
            })

        return Response(serializer.errors, status=400)

