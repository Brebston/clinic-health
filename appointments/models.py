from __future__ import annotations

from datetime import date, time
from django.conf import settings
from django.db import models
from django.utils import timezone

from doctors.models import DoctorProfile


class Appointment(models.Model):
    """
    Appointment with a doctor.

    We store date and time separately because the UI works with <input type="date">
    and <select> time slots. If you later switch to DateTimeField (starts_at),
    this model can be simplified.
    """

    STATUS_BOOKED = "booked"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = (
        (STATUS_BOOKED, "Booked"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_BOOKED)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-appointment_date", "-appointment_time")
        constraints = [
            models.UniqueConstraint(
                fields=("doctor", "appointment_date", "appointment_time"),
                name="uniq_doctor_day_time",
            )
        ]

    def __str__(self) -> str:
        return f"{self.patient} -> {self.doctor} @ {self.appointment_date} {self.appointment_time}"

    @property
    def starts_at(self):
        """Return aware datetime for comparisons."""
        naive = timezone.datetime.combine(self.appointment_date, self.appointment_time)
        return timezone.make_aware(naive, timezone.get_current_timezone())

    def is_past(self) -> bool:
        return self.starts_at <= timezone.now()
