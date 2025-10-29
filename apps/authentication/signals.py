from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from apps.customer.models import Customer



@receiver(post_save, sender=User)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Customer.objects.create(user=instance)