from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AccountsViewsTests(TestCase):
    """Few tests to check account pages work."""

    def test_register_redirects_to_profile(self):
        resp = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "registered",
                "first_name": "Reg",
                "last_name": "User",
                "email": "reg@example.com",
                "phone": 555123123,
                "date_of_birth": "2000-01-01",
                "ssn": "SSN",
                "address": "Addr",
                "emergency_contact_name": "Contact",
                "emergency_contact_phone": "123",
                "password1": "Test123!",
                "password2": "Test123!",
            },
            follow=False,
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/profile/", resp["Location"])

    def test_login_with_email_works(self):
        user = User.objects.create_user(
            username="loginuser",
            email="login@gmail.com",
            password="pass12345!",
        )
        resp = self.client.post(
            reverse("accounts:login"),
            data={"username": "login@gmail.com", "password": "pass12345!"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/profile/", resp["Location"])

    def test_profile_requires_authentication(self):
        user = User.objects.create_user(
            username="private",
            email="private@gmail.com",
            password="pass12345!",
        )
        resp = self.client.get(reverse("accounts:profile", kwargs={"pk": user.pk}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp["Location"])