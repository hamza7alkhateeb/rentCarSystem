from .models import Customer
from django.core.exceptions import ObjectDoesNotExist

class CustomerRepo:
    """ Repository class that handles all database operations related to the Customer model.
    It separates data access logic from the main application logic."""

    def get_by_user(self, user):
        """ Retrieves a Customer instance based on the given user.
        Returns None if no matching customer is found instead of raising an exception."""
        try:
            return Customer.objects.get(user=user)
        except ObjectDoesNotExist:
            return None

    def update(self, customer, data):
        """ Updates the fields of a given customer instance with the provided data
         After updating all fields, it saves the customer and returns the updated object"""
        for field, value in data.items():
            setattr(customer, field, value)
        customer.save()
        return customer

