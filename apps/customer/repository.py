from .models import Customer
from django.core.exceptions import ObjectDoesNotExist

class CustomerRepo:

    def get_by_user(self, user):
        try:
            return Customer.objects.get(user=user)
        except ObjectDoesNotExist:
            return None

    def update(self, customer, data):
        for field, value in data.items():
            setattr(customer, field, value)
        customer.save()
        return customer

