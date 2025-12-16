from django import forms

from doctors.models import DoctorProfile


class IndexDoctorSearchForm(forms.Form):
    doctor_name = forms.CharField(
        max_length=255,
        required=False,
    )
    specialty = forms.ChoiceField(
        required=False,
        choices=[("", "All Specialties")] + list(DoctorProfile.Specialty.choices),
    )