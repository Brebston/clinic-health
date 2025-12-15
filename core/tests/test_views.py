from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from doctors.models import DoctorProfile


User = get_user_model()


class IndexViewTests(TestCase):
    """Tests for the homepage doctor list"""

    def setUp(self):
        self.doctor_user_1 = User.objects.create_user(
            username="doc1",
            email="doc1@example.com",
            password="pass12345!",
            role=User.Roles.DOCTOR,
            first_name="Alice",
            last_name="Anderson",
        )
        self.doctor_user_2 = User.objects.create_user(
            username="doc2",
            email="doc2@example.com",
            password="pass12345!",
            role=User.Roles.DOCTOR,
            first_name="Bob",
            last_name="Brown",
        )

        DoctorProfile.objects.create(
            user=self.doctor_user_1,
            specialty=DoctorProfile.Specialty.CARDIOLOGIST,
            department=DoctorProfile.Department.CARDIOLOGY,
            description="Bio",
            years_of_experience=5,
        )
        DoctorProfile.objects.create(
            user=self.doctor_user_2,
            specialty=DoctorProfile.Specialty.NEUROLOGIST,
            department=DoctorProfile.Department.NEUROLOGY,
            description="Bio",
            years_of_experience=6,
        )

    def test_index_page_loads(self):
        resp = self.client.get(reverse("core:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("doctor_list", resp.context)

    def test_filter_by_specialty(self):
        resp = self.client.get(
            reverse("core:index"),
            {"specialty": DoctorProfile.Specialty.CARDIOLOGIST},
        )
        self.assertEqual(resp.status_code, 200)
        doctor_list = list(resp.context["doctor_list"])
        self.assertEqual(len(doctor_list), 1)
        self.assertEqual(doctor_list[0].user.username, "doc1")

    def test_filter_by_name_matches_first_or_last(self):
        resp = self.client.get(reverse("core:index"), {"doctor_name": "bro"})
        self.assertEqual(resp.status_code, 200)
        doctor_list = list(resp.context["doctor_list"])
        self.assertEqual(len(doctor_list), 1)
        self.assertEqual(doctor_list[0].user.username, "doc2")

    def test_htmx_request_renders_partial_template(self):
        resp = self.client.get(
            reverse("core:index"),
            {"specialty": DoctorProfile.Specialty.NEUROLOGIST},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/doctor_list.html")


class DoctorsBySpecialtyViewTests(TestCase):
    """Tests for the doctors AJAX endpoint"""

    def setUp(self):
        self.doc_user = User.objects.create_user(
            username="ajaxdoc",
            email="ajaxdoc@example.com",
            password="pass12345!",
            role=User.Roles.DOCTOR,
            first_name="Charlie",
            last_name="Chaplin",
        )
        self.doc_profile = DoctorProfile.objects.create(
            user=self.doc_user,
            specialty=DoctorProfile.Specialty.DERMATOLOGIST,
            department=DoctorProfile.Department.DERMATOLOGY,
            description="Bio",
            years_of_experience=4,
        )

    def test_returns_empty_when_no_specialty(self):
        resp = self.client.get(reverse("doctors:doctors-by-specialty"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"doctors": []})

    def test_returns_doctors_for_specialty(self):
        resp = self.client.get(
            reverse("doctors:doctors-by-specialty"),
            {"specialty": DoctorProfile.Specialty.DERMATOLOGIST},
        )
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertIn("doctors", payload)
        self.assertEqual(len(payload["doctors"]), 1)
        self.assertEqual(payload["doctors"][0]["id"], self.doc_profile.id)
        self.assertIn("Dr.", payload["doctors"][0]["name"])