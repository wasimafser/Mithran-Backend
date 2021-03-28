from django.contrib import admin

from .models import ServiceStatus, Service

# Register your models here.
admin.site.register(ServiceStatus)
admin.site.register(Service)
