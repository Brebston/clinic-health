from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from core.forms import IndexDoctorSearchForm
from doctors.models import DoctorProfile


class IndexView(generic.ListView):
    model = DoctorProfile
    template_name = "core/index.html"
    context_object_name = "doctor_list"

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["search_form"] = IndexDoctorSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = DoctorProfile.objects.select_related("user")
        form = IndexDoctorSearchForm(self.request.GET)
        if not form.is_valid():
            return queryset

        doctor_name = (form.cleaned_data.get("doctor_name") or "").strip()
        specialty = form.cleaned_data.get("specialty") or ""

        if specialty:
            queryset = queryset.filter(specialty=specialty)

        if doctor_name:
            queryset = queryset.filter(
                Q(user__first_name__icontains=doctor_name) |
                Q(user__last_name__icontains=doctor_name)
                )

        return queryset

    """
    Fixing the eternal loading screen when searching for doctors
    """
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request") == "true":
            return render(self.request, "includes/doctor_list.html", context)
        return super().render_to_response(context, **response_kwargs)

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
    return render(request, "core/appointment.html", {
        "specialties": DoctorProfile.Specialty.choices,
    })

def testimonials_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/testimonials.html")

def faq_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/faq.html")

def terms_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html")

def privacy_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html")