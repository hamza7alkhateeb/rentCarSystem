from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Booking

@receiver(pre_save, sender=Booking)
def calculate_total_price(sender, instance):
    if instance.start_date and instance.end_date and instance.vehicle and instance.vehicle.daily_rate:
        days = max((instance.end_date - instance.start_date).days, 1)
        instance.total_price = days * instance.vehicle.daily_rate
