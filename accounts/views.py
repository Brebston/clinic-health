from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm
from .models import Patient


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return redirect(reverse(
            "accounts:profile",
            kwargs={"pk": self.object.pk}
        ))


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient
    template_name = "accounts/profile.html"


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Patient
    template_name = "accounts/profile_form.html"
    fields = ("username", "first_name", "last_name", "email", "phone", "address", "ssn", "emergency_contact_name", "emergency_contact_phone", )

    def get_success_url(self):
        return reverse(
            "accounts:profile",
            kwargs={"pk": self.request.user.pk}
        )


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse(
            "accounts:profile",
            kwargs={"pk": self.request.user.pk}
        )
