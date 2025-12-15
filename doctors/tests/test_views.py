from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from doctors.models import DoctorProfile


User = get_user_model()


class DoctorsBySpecialtyViewTests(TestCase):
    """Basic tests for doctors_by_specialty view"""

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username="doc1",
            password="pass12345!",
            role=User.Roles.DOCTOR,
            first_name="John",
            last_name="Smith",
        )

        self.profile = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty=DoctorProfile.Specialty.CARDIOLOGIST,
            department=DoctorProfile.Department.CARDIOLOGY,
            description="Test doctor",
            years_of_experience=5,
        )

    def test_returns_empty_list_if_no_specialty(self):
        """If no specialty is provided then doctors list should be empty"""
        resp = self.client.get(reverse("doctors:doctors-by-specialty")
)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"doctors": []})

    def test_returns_empty_list_for_unknown_specialty(self):
        """Unknown specialty should return empty doctors list."""
        resp = self.client.get(
            reverse("doctors:doctors-by-specialty"),
            {"specialty": "unknown"},
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"doctors": []})
