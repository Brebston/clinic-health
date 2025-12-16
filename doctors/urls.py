from django.urls import path
from doctors.views import doctors_by_specialty


urlpatterns = [
    path("ajax/doctors-by-specialty/", doctors_by_specialty, name="doctors-by-specialty"),
]

app_name = "doctors"
