from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Consumer, Worker, WorkerSpecialization

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'full_name')}),
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

admin.site.register(Consumer)
admin.site.register(Worker)
admin.site.register(WorkerSpecialization)
