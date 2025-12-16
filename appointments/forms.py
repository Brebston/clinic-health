from __future__ import annotations

from datetime import date, datetime, time
from django import forms
from django.utils import timezone

from doctors.models import DoctorProfile


class AppointmentCreateForm(forms.Form):
    """
    Simple form for booking an appointment.

    doctor: DoctorProfile id
    day: date
    time_str: 'HH:MM'
    notes: optional
    """

    doctor = forms.ModelChoiceField(queryset=DoctorProfile.objects.select_related("user"))
    day = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time_str = forms.CharField(max_length=5)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def clean_day(self) -> date:
        d = self.cleaned_data["day"]
        if d < timezone.localdate():
            raise forms.ValidationError("Date cannot be in the past.")
        return d

    def clean_time_str(self) -> str:
        t = self.cleaned_data["time_str"].strip()
        try:
            hh, mm = t.split(":")
            time(int(hh), int(mm))
        except Exception:
            raise forms.ValidationError("Invalid time format. Use HH:MM.")
        return t

    def build_starts_at(self) -> datetime:
        d = self.cleaned_data["day"]
        t = self.cleaned_data["time_str"]
        hh, mm = t.split(":")
        naive = datetime.combine(d, time(int(hh), int(mm)))
        return timezone.make_aware(naive, timezone.get_current_timezone())
