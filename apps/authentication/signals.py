from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from apps.customer.models import Customer


@receiver(post_save, sender=User)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    """
    Automatically create a Customer profile when a new non-staff User is created.

    Triggered:
        - After a User instance is saved (post_save signal).
    
    Conditions:
        - Runs only when a new user is created (`created=True`)
        - Excludes admin/staff/superuser accounts

    Parameters:
        sender (Model): The model class sending the signal (User)
        instance (User): The actual User instance that was saved
        created (bool): True if the instance was created (not updated)
        **kwargs: Additional keyword arguments passed by the signal

    Behavior:
        - Creates a related Customer object automatically linked to the user.
    """
    if created and not instance.is_staff and not instance.is_superuser:
        Customer.objects.create(user=instance)
