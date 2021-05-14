from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets[2][1]["fields"] = (
    'is_active', 
    'is_superuser',
    'ip_address', 
)

UserAdmin.list_display = (
    "username",
    "is_superuser",
    "ip_address",
)

admin.site.register(User, UserAdmin)