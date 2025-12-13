from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from doctors.models import DoctorProfile


def index (request: HttpRequest) -> HttpResponse:
    return render(request, "core/index.html")


def about_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")

def departament_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/departments.html")

def services_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/services.html")

class DoctorView(generic.ListView):
    model = DoctorProfile
    template_name = "core/doctors.html"
    context_object_name = "doctors_list"

def contact_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")

def department_details_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/department-details.html")

def service_details_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/service-details.html")

def appointment_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/appointment.html")

def testimonials_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/testimonials.html")

def faq_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/faq.html")

def terms_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html")

def privacy_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html")