from django.urls import path
from core.views import (IndexView, about_page,
                        departament_page, services_page,
                        DoctorView, contact_page,
                        department_details_page, service_details_page,
                        appointment_page, testimonials_page,
                        faq_page, terms_page,
                        privacy_page)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", about_page, name="about"),
    path("departaments/", departament_page, name="departament"),
    path("services/", services_page, name="services"),
    path("doctors/", DoctorView.as_view(), name="doctors"),
    path("contact/", contact_page, name="contact"),
    path("department-details/", department_details_page, name="department-details"),
    path("service-details/", service_details_page, name="service-details"),
    path("appointment/", appointment_page, name="appointment"),
    path("testimonials/", testimonials_page, name="testimonials"),
    path("faq/", faq_page, name="faq"),
    path("terms/", terms_page, name="terms"),
    path("privacy/", privacy_page, name="privacy")


]

app_name = "core"