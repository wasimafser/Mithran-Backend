from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.base_user import BaseUserManager


# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        last_name = extra_fields.get('last_name', None)
        if last_name:
            full_name = f"{first_name} {last_name}"
            user.last_name = last_name
        else:
            full_name = f"{first_name}"
        user.first_name = first_name
        user.full_name = full_name
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser must have is_active=True")
        return self.create_user(email, first_name, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("Email Address", unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
