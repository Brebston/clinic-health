from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from doctors.models import DoctorProfile


User = get_user_model()


class DoctorProfileModelTests(TestCase):
    """Tests for DoctorProfile model"""

    def test_create_doctor_profile_ok(self):
        """It should create doctor profile for user with DOCTOR role."""
        user = User.objects.create_user(
            username="doc1",
            password="pass12345!",
            email="doc1@example.com",
            role=User.Roles.DOCTOR,
            first_name="John",
            last_name="Smith",
        )

        profile = DoctorProfile.objects.create(
            user=user,
            specialty=DoctorProfile.Specialty.CARDIOLOGIST,
            department=DoctorProfile.Department.CARDIOLOGY,
            description="Some description",
            years_of_experience=3,
        )

        profile.clean()

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.specialty, DoctorProfile.Specialty.CARDIOLOGIST)
        self.assertEqual(profile.department, DoctorProfile.Department.CARDIOLOGY)
        self.assertEqual(profile.years_of_experience, 3)

    def test_clean_fails_if_user_not_doctor(self):
        """Profile should not work if user role is not doctor"""
        user = User.objects.create_user(
            username="pat1",
            password="pass12345!",
            email="pat1@example.com",
            role=User.Roles.PATIENT,
            first_name="Pat",
            last_name="User",
        )

        profile = DoctorProfile(
            user=user,
            specialty=DoctorProfile.Specialty.NEUROLOGIST,
            department=DoctorProfile.Department.NEUROLOGY,
            description="Desc",
            years_of_experience=1,
        )

        with self.assertRaises(ValidationError):
            profile.clean()

    def test_is_online_false_when_no_last_seen(self):
        """If last_seen is empty then is_online should be False."""
        user = User.objects.create_user(
            username="doc2",
            password="pass12345!",
            email="doc2@example.com",
            role=User.Roles.DOCTOR,
        )
        profile = DoctorProfile.objects.create(
            user=user,
            specialty=DoctorProfile.Specialty.DERMATOLOGIST,
            department=DoctorProfile.Department.DERMATOLOGY,
            description="Desc",
            years_of_experience=5,
        )

        self.assertFalse(profile.is_online)

    def test_is_online_true_when_last_seen_recent(self):
        """If last_seen is recent then is_online should be True"""
        user = User.objects.create_user(
            username="doc3",
            password="pass12345!",
            email="doc3@example.com",
            role=User.Roles.DOCTOR,
        )
        profile = DoctorProfile.objects.create(
            user=user,
            specialty=DoctorProfile.Specialty.EMERGENCY,
            department=DoctorProfile.Department.EMERGENCY,
            description="Desc",
            years_of_experience=2,
            last_seen=timezone.now() - timedelta(minutes=2),
        )

        self.assertTrue(profile.is_online)

    def test_stars_ceil(self):
        """Check stars rounding"""
        user = User.objects.create_user(
            username="doc4",
            password="pass12345!",
            email="doc4@example.com",
            role=User.Roles.DOCTOR,
        )
        profile = DoctorProfile.objects.create(
            user=user,
            specialty=DoctorProfile.Specialty.RADIOLOGIST,
            department=DoctorProfile.Department.RADIOLOGY,
            description="Desc",
            years_of_experience=7,
        )

        self.assertEqual(profile.stars_ceil, 0)

        profile.stars = 4.2
        self.assertEqual(profile.stars_ceil, 5)  # ceil(4.2) = 5

        profile.stars = 5.0
        self.assertEqual(profile.stars_ceil, 5)

        profile.stars = 10
        self.assertEqual(profile.stars_ceil, 5)  # max 5

    def test_str(self):
        """Simple __str__ test."""
        user = User.objects.create_user(
            username="doc5",
            password="pass12345!",
            email="doc5@example.com",
            role=User.Roles.DOCTOR,
            first_name="Anna",
            last_name="Nowak",
        )
        profile = DoctorProfile.objects.create(
            user=user,
            specialty=DoctorProfile.Specialty.PEDIATRICIAN,
            department=DoctorProfile.Department.PEDIATRICS,
            description="Desc",
            years_of_experience=1,
        )

        self.assertEqual(str(profile), "Dr. Anna Nowak")
