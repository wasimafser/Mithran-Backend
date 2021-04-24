from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from user_management.models import Profile, WorkerSpecialization

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
    assigned_on = models.DateTimeField(auto_now_add=True)
    started_on = models.DateTimeField(blank=True, null=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    total_work_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"{self.requested_by.user.full_name} - {self.type.name}"


class ServiceState(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    consumer_started = models.BooleanField(default=False)
    worker_started = models.BooleanField(default=False)
    consumer_completed = models.BooleanField(default=False)
    worker_completed = models.BooleanField(default=False)


@receiver(post_save, sender=Service)
def create_profile(sender, instance, created, **kwargs):
    if created:
        service = Service.objects.get(pk=instance.id)
        service.status = ServiceStatus.objects.get(name__icontains='ASSIGNED')
        service.save()

        ServiceState.objects.create(
            service=service
        )
    print(instance)


@receiver(post_save, sender=ServiceState)
def update_service_state(sender, instance, created, **kwargs):
    service = Service.objects.get(pk=instance.service.id)
    ASSIGNED = ServiceStatus.objects.get(
        name__icontains="ASSIGNED"
    )
    WIP = ServiceStatus.objects.get(
        name__icontains="WORK IN PROGRESS"
    )
    RESOLVED = ServiceStatus.objects.get(name__icontains="RESOLVED")
    if instance.consumer_started and instance.worker_started and service.status == ASSIGNED:
        service.started_on = timezone.now()
        service.status = WIP
        service.save()
    if instance.consumer_completed and instance.worker_completed and service.status == WIP:
        service = Service.objects.get(pk=instance.service.id)
        service.completed_on = timezone.now()
        service.total_work_time = service.completed_on - service.started_on
        service.status = RESOLVED
        service.save()
