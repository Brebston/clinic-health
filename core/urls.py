from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path
from core.views import index, about_page, departament_page, services_page, doctors_page

urlpatterns = [
    path("", index, name="index"),
    path("about/", about_page, name="about-page"),
    path("departaments/", departament_page, name="departament-page"),
    path("services/", services_page, name="services-page"),
    path("doctors/", doctors_page, name="doctors-page")
] + debug_toolbar_urls()

app_name = "core"