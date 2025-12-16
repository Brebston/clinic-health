from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class LastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                doctor_profile = request.user.doctor_profile
            except ObjectDoesNotExist:
                return response

            doctor_profile.last_seen = timezone.now()
            doctor_profile.save(update_fields=["last_seen"])

        return response
