"""Admin configuration for CustomUser."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'mobile', 'display_name', 'is_staff', 'is_premium', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_premium', 'is_mobile_verified', 'is_email_verified')
    search_fields = ('email', 'mobile', 'display_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'mobile', 'password')}),
        ('Profile', {'fields': ('display_name', 'avatar', 'bio')}),
        ('Verification', {'fields': ('is_mobile_verified', 'is_email_verified', 'otp_code')}),
        ('Subscriptions', {'fields': ('subscribed_newsletter', 'is_premium')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'display_name', 'password1', 'password2'),
        }),
    )
