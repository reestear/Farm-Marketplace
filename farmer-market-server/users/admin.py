from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class AdminUser(UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )
    list_display_links = (
        "id",
        "email",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Персональная информация",
            {
                "fields": (
                    "phone_number",
                    "is_active",
                )
            },
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_type",
                )
            },
        ),
    )

    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                    "phone_number",
                    "is_active",
                ),
            },
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_type",
                    "farmer_status",
                )
            },
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "is_superuser",
        "is_staff",
    )

    ordering = ("email",)
