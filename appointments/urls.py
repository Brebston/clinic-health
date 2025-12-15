from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.appointment_create, name="create"),
    path("my/", views.my_visits, name="my-visits"),

    path("<int:pk>/cancel/", views.cancel_visit, name="cancel-visit"),
    path("<int:pk>/update-status/", views.update_status, name="update-status"),

    # API endpoints for JS on booking page
    path("api/doctors-by-specialty/", views.api_doctors_by_specialty, name="api-doctors-by-specialty"),
    path("api/available-times/", views.api_available_times, name="api-available-times"),
]

app_name = "appointments"