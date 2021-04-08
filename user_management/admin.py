from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, WorkerSpecialization, Organization

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'full_name', 'type')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superuser', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(WorkerSpecialization)
admin.site.register(Organization)
