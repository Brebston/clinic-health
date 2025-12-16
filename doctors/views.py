from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import DoctorProfile


@require_GET
def doctors_by_specialty(request):
    specialty = request.GET.get("specialty")
    if not specialty:
        return JsonResponse({"doctors": []})

    queryset = (DoctorProfile.objects
          .select_related("user")
          .filter(specialty=specialty)
          .order_by("user__last_name", "user__first_name"))

    doctors = [
        {"id": doctor.id, "name": f"Dr. {doctor.user.get_full_name() or doctor.user.username}"}
        for doctor in queryset
    ]
    return JsonResponse({"doctors": doctors})
