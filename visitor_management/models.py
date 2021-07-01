from django.db import models

from user_management.models import Profile

# Create your models here.

class Visitor(models.Model):
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    visiting = models.ForeignKey(Profile, on_delete=models.CASCADE)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.full_name
