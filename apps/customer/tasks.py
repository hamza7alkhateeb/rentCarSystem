from celery import shared_task
from .models import Customer
from .external_api import get_customer_status_mock


@shared_task
def sync_customers_status_task():
    customers = Customer.objects.all()
    updated = 0
    for customer in customers:
        new_status = get_customer_status_mock(customer.id)
        customer.status=new_status
        customer.save()
        updated += 1

    return f"{updated} customers status updated successfully"

@shared_task
def sync_single_customer_status_task(customer_id):

    customer = Customer.objects.get(id=customer_id)

    new_status = get_customer_status_mock(customer.id)
    customer.status = new_status
    customer.save()

    return f"Customer {customer_id} status updated successfully"
