from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

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


class Profile(models.Model):
    contact_number = models.CharField(max_length=20)
    alternate_contact_number = models.CharField(max_length=20, null=True, blank=True)
    door_number = models.CharField(max_length=100)
    address = models.CharField(max_length=225)

    class Meta:
        abstract = True


class Organization(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    url = models.URLField(max_length=225)

    def __str__(self):
        return f"{self.name} - {self.code}"


class Consumer(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    def __str__(self):
        return self.user.full_name


class WorkerSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    specializations = models.ManyToManyField(WorkerSpecialization)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    def __str__(self):
        return self.user.full_name


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs=True):
#     if created:
#
