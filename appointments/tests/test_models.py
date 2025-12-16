from __future__ import annotations

"""
Tests for Appointment model
"""

from datetime import timedelta, time as dt_time

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from appointments.models import Appointment
from doctors.models import DoctorProfile

User = get_user_model()


class TestAppointmentModel(TestCase):
    """Basic tests for Appointment model"""

    def setUp(self) -> None:
        """Create a patient and a doctor profile"""
        self.patient = User.objects.create_user(
            username="patient1",
            email="patient@test.com",
            password="12345",
        )
        self.doctor_user = User.objects.create_user(
            username="doctor1",
            email="doctor@test.com",
            password="12345",
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            years_of_experience=1,
        )

    def test_str(self) -> None:
        """__str__ should contain patient, doctor and date/time"""
        day = timezone.localdate() + timedelta(days=2)
        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=day,
            appointment_time=dt_time(10, 30),
        )

        text = str(appt)
        self.assertIn("patient1", text)
        self.assertIn(str(self.doctor), text)
        self.assertIn(str(day), text)
        self.assertIn("10:30:00", text)

    def test_starts_at_is_aware(self) -> None:
        """starts_at should return timezone-aware datetime"""
        day = timezone.localdate() + timedelta(days=1)
        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=day,
            appointment_time=dt_time(9, 0),
        )

        starts = appt.starts_at
        self.assertTrue(timezone.is_aware(starts))
        self.assertEqual(starts.hour, 9)
        self.assertEqual(starts.minute, 0)

    def test_is_past_true_for_old_appointment(self) -> None:
        """is_past should be True for appointment in the past"""
        yesterday = timezone.localdate() - timedelta(days=1)
        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=yesterday,
            appointment_time=dt_time(10, 0),
        )
        self.assertTrue(appt.is_past())

    def test_is_past_false_for_future_appointment(self) -> None:
        """is_past should be False for appointment in the future"""
        tomorrow = timezone.localdate() + timedelta(days=1)
        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=tomorrow,
            appointment_time=dt_time(10, 0),
        )
        self.assertFalse(appt.is_past())

    def test_unique_constraint_doctor_day_time(self) -> None:
        """Should not allow two appointments with same doctor/date/time"""
        day = timezone.localdate() + timedelta(days=3)
        t = dt_time(11, 0)

        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=day,
            appointment_time=t,
        )

        with self.assertRaises(IntegrityError):
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                appointment_date=day,
                appointment_time=t,
            )
