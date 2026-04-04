from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


def apply_bootstrap_style(form):
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control',})


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_style(self)


class SignInForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_style(self)
