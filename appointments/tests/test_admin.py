from __future__ import annotations

"""
Tests for Django admin configuration

These tests are simple and just check that Appointment is registered
and that admin options are set as expected
"""

from django.contrib import admin
from django.test import TestCase

from appointments.admin import AppointmentAdmin
from appointments.models import Appointment


class TestAppointmentAdmin(TestCase):
    """Tests for AppointmentAdmin"""

    def test_appointment_is_registered_in_admin(self) -> None:
        """Appointment model should be registered in admin site."""
        self.assertIn(Appointment, admin.site._registry)

    def test_registered_admin_class_is_correct(self) -> None:
        """Registered admin class for Appointment should be AppointmentAdmin."""
        registered_admin = admin.site._registry[Appointment]
        self.assertIsInstance(registered_admin, AppointmentAdmin)

    def test_list_display(self) -> None:
        """Admin list_display should match config"""
        registered_admin = admin.site._registry[Appointment]
        self.assertEqual(
            registered_admin.list_display,
            (
                "id",
                "patient",
                "doctor",
                "appointment_date",
                "appointment_time",
                "status",
                "created_at",
            ),
        )

    def test_list_filter(self) -> None:
        """Admin list_filter should match config"""
        registered_admin = admin.site._registry[Appointment]
        self.assertEqual(
            registered_admin.list_filter,
            ("status", "appointment_date", "doctor"),
        )

    def test_search_fields(self) -> None:
        """Admin search_fields should match config"""
        registered_admin = admin.site._registry[Appointment]
        self.assertEqual(
            registered_admin.search_fields,
            (
                "patient__username",
                "patient__email",
                "doctor__user__username",
                "doctor__user__email",
            ),
        )

    def test_ordering(self) -> None:
        """Admin ordering should match config"""
        registered_admin = admin.site._registry[Appointment]
        self.assertEqual(
            registered_admin.ordering,
            ("-appointment_date", "-appointment_time"),
        )

    def test_autocomplete_fields(self) -> None:
        """Admin autocomplete_fields should match config"""
        registered_admin = admin.site._registry[Appointment]
        self.assertEqual(registered_admin.autocomplete_fields, ("patient", "doctor"))
