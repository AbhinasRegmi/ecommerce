from django.contrib import admin
from .models import UserBase

@admin.register(UserBase)
class BaseUserAdminConfig(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['password']