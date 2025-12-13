from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic


def index (request: HttpRequest) -> HttpResponse:
    return render(request, "core/index.html")


def about_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")

def departament_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/departments.html")

def services_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/services.html")

def doctors_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/doctors.html")

def contact_page(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")
