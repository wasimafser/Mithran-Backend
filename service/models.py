from django.db import models

from user_management.models import Consumer, Worker, WorkerSpecialization

# Create your models here.

# class Type(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    requested_by = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name='+')
    assigned_to = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    type = models.ForeignKey(WorkerSpecialization, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.requested_by.full_name} - {self.type.name}"
