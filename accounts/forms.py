from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Patient
import logging
logger = logging.getLogger(__name__)

User = get_user_model()


class BootstrapMixin:
    """Додає bootstrap-класи до всіх полів форми."""
    def _apply_bootstrap(self):
        for name, field in self.fields.items():
            widget = field.widget
            base = widget.attrs.get("class", "")
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs["class"] = (base + " form-check-input").strip()
            else:
                widget.attrs["class"] = (base + " form-control").strip()
            if "placeholder" not in widget.attrs and field.label:
                widget.attrs["placeholder"] = field.label


class LoginForm(BootstrapMixin, AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class RegisterForm(BootstrapMixin, UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    ssn = forms.CharField(required=True, max_length=20)
    address = forms.CharField(required=True)
    emergency_contact_name = forms.CharField(required=True, max_length=255)
    emergency_contact_phone = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data.get("phone", "")
        user.role = User.Roles.PATIENT
        user.date_of_birth = self.cleaned_data.get("date_of_birth")
        user.ssn = self.cleaned_data.get("ssn", "")
        user.address = self.cleaned_data.get("address", "")
        user.emergency_contact_name = self.cleaned_data.get("emergency_contact_name", "")
        user.emergency_contact_phone = self.cleaned_data.get("emergency_contact_phone", "")

        if commit:
            user.save()
        return user
