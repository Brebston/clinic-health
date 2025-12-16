from __future__ import annotations

"""
Views tests for appointments.
"""

from datetime import timedelta, time as dt_time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from appointments.models import Appointment
from doctors.models import DoctorProfile

User = get_user_model()


class TestAppointmentViews(TestCase):
    """Basic tests for appointment views"""

    def setUp(self) -> None:
        """Create patient user and doctor user/profile"""
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
            specialty=DoctorProfile.Specialty.CARDIOLOGIST,
            department=DoctorProfile.Department.CARDIOLOGY,
        )

    # ---------- appointment_create ----------

    def test_appointment_create_get_requires_login(self) -> None:
        """GET booking page should redirect if not logged in"""
        url = reverse("appointments:create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_appointment_create_get_ok(self) -> None:
        """GET booking page should return 200 when logged in"""
        self.client.login(username="patient1", password="12345")
        url = reverse("appointments:create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_appointment_create_post_invalid_form(self) -> None:
        """POST with invalid form should return 400"""
        self.client.login(username="patient1", password="12345")
        url = reverse("appointments:create")

        resp = self.client.post(url, data={})
        self.assertEqual(resp.status_code, 400)

    def test_appointment_create_post_cannot_book_past(self) -> None:
        """POST should block booking in the past"""
        self.client.login(username="patient1", password="12345")
        url = reverse("appointments:create")

        yesterday = timezone.localdate() - timedelta(days=1)
        resp = self.client.post(
            url,
            data={
                "doctor": self.doctor.id,
                "day": yesterday,
                "time_str": "10:00",
                "notes": "hi",
            },
        )
        self.assertEqual(resp.status_code, 400)

    def test_appointment_create_post_ok_creates_appointment(self) -> None:
        """Valid POST should create appointment and redirect"""
        self.client.login(username="patient1", password="12345")
        url = reverse("appointments:create")

        future_day = timezone.localdate() + timedelta(days=2)

        resp = self.client.post(
            url,
            data={
                "doctor": self.doctor.id,
                "day": future_day,
                "time_str": "10:00",
                "notes": "some notes",
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 1)

        appt = Appointment.objects.first()
        self.assertEqual(appt.patient, self.patient)
        self.assertEqual(appt.doctor, self.doctor)
        self.assertEqual(appt.appointment_date, future_day)
        self.assertEqual(appt.appointment_time, dt_time(10, 0))
        self.assertEqual(appt.status, Appointment.STATUS_BOOKED)

    def test_appointment_create_post_slot_already_booked(self) -> None:
        """Should return 400 if slot already booked"""
        self.client.login(username="patient1", password="12345")
        url = reverse("appointments:create")

        future_day = timezone.localdate() + timedelta(days=3)
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_day,
            appointment_time=dt_time(11, 0),
            status=Appointment.STATUS_BOOKED,
        )

        resp = self.client.post(
            url,
            data={
                "doctor": self.doctor.id,
                "day": future_day,
                "time_str": "11:00",
            },
        )
        self.assertEqual(resp.status_code, 400)

    # ---------- my_visits ----------

    def test_my_visits_patient_shows_only_own(self) -> None:
        """Patient should see only their visits"""
        other = User.objects.create_user(username="patient2", password="12345")

        day = timezone.localdate() + timedelta(days=5)
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=day,
            appointment_time=dt_time(10, 0),
        )
        Appointment.objects.create(
            patient=other,
            doctor=self.doctor,
            appointment_date=day,
            appointment_time=dt_time(10, 30),
        )

        self.client.login(username="patient1", password="12345")
        url = reverse("appointments:my-visits")