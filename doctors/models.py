from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class DoctorProfile(models.Model):
    class Specialty(models.TextChoices):
        CARDIOLOGIST = "cardiologist", "Cardiologist"
        NEUROLOGIST = "neurologist", "Neurologist"
        ORTHOPEDIC = "orthopedic", "Orthopedic Surgeon"
        PEDIATRICIAN = "pediatrician", "Pediatrician"
        DERMATOLOGIST = "dermatologist", "Dermatologist"
        ONCOLOGIST = "oncologist", "Oncologist"
        EMERGENCY = "emergency", "Emergency Medicine"
        RADIOLOGIST = "radiologist", "Radiologist"

    class Department(models.TextChoices):
        CARDIOLOGY = "cardiology", "Cardiology Dept."
        NEUROLOGY = "neurology", "Neurology Dept."
        ORTHOPEDICS = "orthopedics", "Orthopedics Dept."
        PEDIATRICS = "pediatrics", "Pediatrics Dept."
        DERMATOLOGY = "dermatology", "Dermatology Dept."
        ONCOLOGY = "oncology", "Oncology Dept."
        EMERGENCY = "emergency", "Emergency Dept."
        RADIOLOGY = "radiology", "Radiology Dept."

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )

    specialty = models.CharField(max_length=30, choices=Specialty.choices)
    department = models.CharField(max_length=30, choices=Department.choices)
    description = models.TextField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    photo = models.ImageField(upload_to="img/doctors", blank=True, null=True)

    def clean(self):
        if self.user.role != self.user.Roles.DOCTOR:
            raise ValidationError("User role must be DOCTOR to have a DoctorProfile.")

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}".strip()
