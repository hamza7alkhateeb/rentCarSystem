from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=300, null=True, blank=True)
    license_image = models.ImageField(upload_to='licenses/', null=True, blank=True)
    driver_license_number = models.CharField(max_length=20, null=True, blank=True )
    date_of_birth = models.DateField(null=True, blank=True)

    def get_incomplete_fields(self):
        missing_fields = []
        if not self.phone_number:
            missing_fields.append("phone_number")
        if not self.address:
            missing_fields.append("address")
        if not self.driver_license_number:
            missing_fields.append("driver_license_number")
        if not self.license_image:
            missing_fields.append("license_image")
        if not self.date_of_birth:
            missing_fields.append("date_of_birth")
        return missing_fields

    def is_profile_complete(self):
        return len(self.get_incomplete_fields()) == 0
    
    def __str__(self):
        return self.user.username
    