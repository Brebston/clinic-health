from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

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
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns