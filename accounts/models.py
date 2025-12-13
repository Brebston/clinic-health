from django.contrib.auth.models import AbstractUser
from django.db import models


class Patient(AbstractUser):
    class Roles(models.TextChoices):
        PATIENT = "patient", "Patient"
        DOCTOR = "doctor", "Doctor"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    ssn = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(
        max_length=255,
        blank=True,
    )
    emergency_contact_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    def __str__(self):
        return f"Patient: {self.get_full_name() or self.username}"