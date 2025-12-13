from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm
from .models import Patient


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        # авто-логін після реєстрації
        login(self.request, self.object)
        return response

class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "accounts/profile.html"
    model = Patient


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})
