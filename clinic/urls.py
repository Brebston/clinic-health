from django.contrib import admin
from django.urls import path, include

from clinic import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("doctors/", include("doctors.urls", namespace="doctors")),
    path("appointments/", include("appointments.urls", namespace="appointments"))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns