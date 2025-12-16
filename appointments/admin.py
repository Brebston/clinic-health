from __future__ import annotations

from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin for appointments.
    """

    list_display = (
        "id",
        "patient",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = ("patient__username", "patient__email", "doctor__user__username", "doctor__user__email")
    ordering = ("-appointment_date", "-appointment_time")
    autocomplete_fields = ("patient", "doctor")
