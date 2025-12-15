from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    """
    Tests related to custom user model behavior.
    """
    def test_create_patient(self):
        """
        Ensure that a user with the role 'patient' is created correctly
        and all provided fields are saved and validated as expected.
        """
        username = "Test"
        password = "Test123!"
        email = "test@gmail.com"
        phone = "112"
        role = "patient"
        date_of_birth = "2000-02-18"
        ssn = "123"
        address = "Test Address"
        emergency_contact_name = "Test"
        emergency_contact_phone = "112"
        patient = get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            role=role,
            date_of_birth=date_of_birth,
            ssn=ssn,
            address=address,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
        )
        self.assertEqual(patient.username, username)
        self.assertTrue(patient.check_password(password))
        self.assertEqual(patient.email, email)
        self.assertEqual(patient.phone, phone)
        self.assertEqual(patient.role, role)
        self.assertEqual(patient.date_of_birth, date_of_birth)
        self.assertEqual(patient.ssn, ssn)
        self.assertEqual(patient.address, address)
        self.assertEqual(patient.emergency_contact_name, emergency_contact_name)
        self.assertEqual(patient.emergency_contact_phone, emergency_contact_phone)

