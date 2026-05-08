from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ('created_at',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'department',
                'password1',
                'password2',
            ),
        }),
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )
        }),

        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'department',
                'telegram_chat_id',
                'telegram_username',
                'vk_user_id',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),

        ('Important dates', {
            'fields': (
                'last_login',
                'date_joined',
                'created_at',
            )
        }),
    )

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'department',
        'is_staff',
        'created_at',
    )

    list_filter = (
        'department',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'telegram_username',
        'telegram_chat_id',
        'vk_user_id',
    )

    ordering = ('username',)