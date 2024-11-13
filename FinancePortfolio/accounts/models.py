from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUsermanager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_main_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_main_admin') is not True:
            raise ValueError('There can only be one main admin.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, error_messages={'unique': "A user with this email already exists."})
    is_main_admin = models.BooleanField(default=False)

    objects = CustomUsermanager()

    def clean(self):
        # validate email format
        if not self.email:
            raise ValidationError(_('Email is required.'))
        if self.is_main_admin and CustomUser.objects.filter(is_main_admin=True).exclude(pk=self.pk).exists():
            raise ValidationError(_('There can only be one main admin.'))

    def __str__(self):
        return self.username
