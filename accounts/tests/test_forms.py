from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import LoginForm, RegisterForm


User = get_user_model()


class BootstrapMixinTests(TestCase):
    """Check that bootstrap classes are added to widgets."""

    def test_login_form_applies_bootstrap_classes(self):
        form = LoginForm()
        self.assertIn("form-control", form.fields["username"].widget.attrs.get("class", ""))
        self.assertIn("form-control", form.fields["password"].widget.attrs.get("class", ""))


class RegisterFormTests(TestCase):
    """Form for entering user data when registering."""

    def _valid_payload(self, **overrides):
        payload = {
            "username": "new_user",
            "first_name": "TestName",
            "last_name": "TestSurname",
            "email": "test@gmail.com",
            "phone": 123456789,
            "date_of_birth": "1999-01-02",
            "ssn": "ABC-123",
            "address": "Test Address",
            "emergency_contact_name": "John Doe",
            "emergency_contact_phone": "+48111222333",
            "password1": "Password123!",
            "password2": "Password123!",
        }
        payload.update(overrides)
        return payload

    def test_valid_form_creates_patient_with_profile_fields(self):
        form = RegisterForm(data=self._valid_payload())
        self.assertTrue(form.is_valid(), msg=form.errors.as_json())

        user = form.save()
        user.refresh_from_db()

        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.phone, str(123456789))
        self.assertEqual(user.role, User.Roles.PATIENT)
        self.assertEqual(user.ssn, "ABC-123")
        self.assertEqual(user.emergency_contact_name, "John Doe")

    def test_password_mismatch_is_invalid(self):
        form = RegisterForm(data=self._valid_payload(password2="DifferentPass123!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)