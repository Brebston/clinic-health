from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from accounts.views import (CustomLoginView, RegisterView,
                            ProfileDetailView, ProfileUpdateView)


urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="accounts/login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("accounts:login")),
        name="logout",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update")
] + debug_toolbar_urls()

app_name = "accounts"