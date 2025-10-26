from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=300, null=True, blank=True)
    license_image = models.ImageField(upload_to='licenses/', null=True, blank=True)
    driver_licens_number = models.CharField(max_length=20, null=True, blank=True )
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    