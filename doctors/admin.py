from django.contrib import admin
from doctors.models import DoctorProfile


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor_name", "specialty", "department", "years_of_experience")
    list_filter = ("specialty", "department", "stars")
    search_fields = ("user__first_name", "user__last_name", "user__username", "user__email")
    autocomplete_fields = ("user",)

    def doctor_name(self, obj):
        fn = obj.user.first_name or ""
        ln = obj.user.last_name or ""
        name = (fn + " " + ln).strip()
        return f"Dr. {name}" if name else f"Dr. {obj.user.username}"
    doctor_name.short_description = "Doctor"
