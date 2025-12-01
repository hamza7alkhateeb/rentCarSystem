from celery import shared_task
from .models import Customer
from .external_api import get_customer_status_mock


@shared_task(name="apps.customer.tasks.sync_customer_status_task")
def sync_customer_status_task():
    print('test')
    customers = Customer.objects.all()
    updated = 0
    for customer in customers:
        new_status = get_customer_status_mock(customer.id)
        customer.status=new_status
        customer.save()
        updated += 1

    return f"{updated} customers status updated successfully"