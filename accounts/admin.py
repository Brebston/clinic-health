from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Patient  # або User, як у тебе називається кастомна модель

@admin.register(Patient)
class PatientAdmin(UserAdmin):
    list_display = ("id", "email", "username", "role", "phone", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "phone", "ssn")
    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {
            "fields": (
                "role",
                "phone",
                "date_of_birth",
                "ssn",
                "address",
                "emergency_contact_name",
                "emergency_contact_phone",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "role",
                "phone",
                "date_of_birth",
                "ssn",
                "address",
                "emergency_contact_name",
                "emergency_contact_phone",
            )
        }),
    )
