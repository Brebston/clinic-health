from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from doctors.models import DoctorProfile
from doctors.admin import DoctorProfileAdmin


User = get_user_model()


class DoctorProfileAdminTests(TestCase):
    """Tests for DoctorProfile admin"""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="pass12345!",
        )
        self.client.login(username="admin", password="pass12345!")

        self.user = User.objects.create_user(
            username="doc1",
            email="doc1@gmail.com",
            password="pass12345!",
            role=User.Roles.DOCTOR,
            first_name="John",
            last_name="Smith",
        )

        self.profile = DoctorProfile.objects.create(
            user=self.user,
            specialty=DoctorProfile.Specialty.CARDIOLOGIST,
            department=DoctorProfile.Department.CARDIOLOGY,
            description="Test",
            years_of_experience=3,
        )

    def test_admin_changelist_page_opens(self):
        """Admin list page should open."""
        url = reverse("admin:doctors_doctorprofile_changelist")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_doctor_name_method(self):
        """doctor_name should show Dr. First Last (or username)."""
        admin_obj = DoctorProfileAdmin(DoctorProfile, admin.site)

        name = admin_obj.doctor_name(self.profile)
        self.assertEqual(name, "Dr. John Smith")

        # if no first/last name, it should use username
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.save()

        name2 = admin_obj.doctor_name(self.profile)
        self.assertEqual(name2, "Dr. doc1")
