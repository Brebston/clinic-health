from django.test import TestCase

from core.forms import IndexDoctorSearchForm


class IndexDoctorSearchFormTests(TestCase):
    """Simple form but needs to be checked."""

    def test_all_specialties_choice_exists(self):
        form = IndexDoctorSearchForm()
        specialty = form.fields["specialty"].choices
        self.assertEqual(specialty[0], ("", "All Specialties"))

    def test_empty_data_is_valid(self):
        form = IndexDoctorSearchForm(data={})
        self.assertTrue(form.is_valid())