from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

user = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=20, required=True, label='Phone No.')
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValueError("A User with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Password do not match")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')
    new_password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            self.add_error('email', "No such user with this email found")

        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Password do not match.")

        return cleaned_data