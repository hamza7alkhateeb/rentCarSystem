import random
from .emums import CustomerStatus

def get_customer_status_mock(customer_id):

    return random.choice([
        CustomerStatus.VERIFIED.value,
        CustomerStatus.UNVERIFIED.value,
        CustomerStatus.BLOCKED.value])