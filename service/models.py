from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_management.models import Profile, Profile, WorkerSpecialization

# Create your models here.

# class Type(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name


class ServiceStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    requested_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    type = models.ForeignKey(WorkerSpecialization, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    status = models.ForeignKey(ServiceStatus, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.requested_by.user.full_name} - {self.type.name}"


@receiver(post_save, sender=Service)
def create_profile(sender, instance, created, **kwargs):
    if created:
        service = Service.objects.get(pk=instance.id)
        service.status = ServiceStatus.objects.get(pk=2)
        service.save()
