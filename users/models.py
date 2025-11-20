from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        STUDENT = "STUDENT", "Student"

    base_role = Role.STUDENT
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.role
        super().save(*args, **kwargs)

    # Add any other custom fields here, e.g.,
    # phone_number = models.CharField(max_length=15, blank=True, null=True)

