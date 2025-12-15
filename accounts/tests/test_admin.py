from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase

from doctors.models import DoctorProfile


User = get_user_model()


class AdminRegistrationTests(TestCase):
    """Basic checks for the configured admin classes."""

    def test_patient_is_registered(self):
        self.assertIn(User, admin.site._registry)

    def test_patient_admin_has_expected_list_display(self):
        patient_admin = admin.site._registry[User]
        for field_name in ("email", "username", "role", "phone"):
            self.assertIn(field_name, patient_admin.list_display)

    def test_doctor_profile_is_registered(self):
        self.assertIn(DoctorProfile, admin.site._registry)

    def test_doctor_profile_admin_has_autocomplete_user(self):
        profile_admin = admin.site._registry[DoctorProfile]
        self.assertIn("user", getattr(profile_admin, "autocomplete_fields", ()))
