from __future__ import annotations

"""
Tests for AppointmentCreateForm

These tests check basic validation logic and helper methods
Written in a simple and straightforward way
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from appointments.forms import AppointmentCreateForm
from doctors.models import DoctorProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAppointmentCreateForm(TestCase):
    """Basic tests for AppointmentCreateForm"""

    def setUp(self) -> None:
        """Create user and doctor profile for tests"""
        self.user = User.objects.create_user(
            username="doctor1",
            email="doc@test.com",
            password="12345",
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.user,
            years_of_experience=1,
        )

    def test_form_valid_data(self) -> None:
        """Form should be valid with correct data"""
        future_day = timezone.localdate() + timedelta(days=1)

        form = AppointmentCreateForm(
            data={
                "doctor": self.doctor.id,
                "day": future_day,
                "time_str": "10:30",
                "notes": "Test notes",
            }
        )

        self.assertTrue(form.is_valid())

    def test_day_cannot_be_in_past(self) -> None:
        """Day in the past should raise validation error"""
        past_day = timezone.localdate() - timedelta(days=1)

        form = AppointmentCreateForm(
            data={
                "doctor": self.doctor.id,
                "day": past_day,
                "time_str": "10:30",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("day", form.errors)

    def test_invalid_time_format(self) -> None:
        """Invalid time format should raise validation error"""
        future_day = timezone.localdate() + timedelta(days=1)

        form = AppointmentCreateForm(
            data={
                "doctor": self.doctor.id,
                "day": future_day,
                "time_str": "abc",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("time_str", form.errors)


    def test_build_starts_at_returns_aware_datetime(self) -> None:
        """build_starts_at should return timezone-aware datetime"""
        future_day = timezone.localdate() + timedelta(days=1)

        form = AppointmentCreateForm(
            data={
                "doctor": self.doctor.id,
                "day": future_day,
                "time_str": "09:00",
            }
        )

        self.assertTrue(form.is_valid())

        starts_at = form.build_starts_at()
        self.assertTrue(timezone.is_aware(starts_at))
        self.assertEqual(starts_at.hour, 9)
        self.assertEqual(starts_at.minute, 0)