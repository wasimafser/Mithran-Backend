from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(ServiceStatus)
admin.site.register(Service)
admin.site.register(ServiceState)
admin.site.register(ServiceFeedback)
