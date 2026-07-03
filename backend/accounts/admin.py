from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import(CustomUser,EmailOTP,LoginAttempt,AuditLog,)

#admin username = test password = 123
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display=(
        "email",
        "username",
        "provider",
        "email_verified",
        "is_active",
        "is_staff",
        "created_at",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    list_filter =(
        "provider",
        "email_verified",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    ordering =(
        "-created_at",
    )

    readonly_fields =(
        "uuid",
        "created_at",
        "updated_at",
        "last_login",
    )

    list_per_page = 25
    date_hierarchy = "created_at"
    
    fieldsets = (
    (
        "Account Information",
        {
            "fields": (
                "uuid",
                "email",
                "username",
                "password",
            )
        },
    ),
    (
        "Profile",
        {
            "fields": (
                "first_name",
                "last_name",
                "profile_picture",
            )
        },
    ),
    (
        "Authentication",
        {
            "fields": (
                "provider",
                "provider_id",
                "email_verified",
            )
        },
    ),
    (
        "Permissions",
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        },
    ),
    (
        "Important Dates",
        {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            )
        },
    ),
)
    add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "password1",
                "password2",
                "provider",
                "email_verified",
            ),
        },
    ),
)
    
@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    
    list_display = (
        "uuid",
        "email",
        "purpose",
        "verified",
        "attempts",
        "resend_count",
        "expires_at",
        "created_at",
    )

    search_fields = (
        "email",
    )

    list_filter = (
        "purpose",
        "verified",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "uuid",
        'otp_hash',
        "created_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"
@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "uuid",
        "email",
        "ip_address",
        "attempts",
        "is_locked",
        "locked_until",
        "last_attempt",
        "created_at",
    )

    search_fields = (
        "email",
        "ip_address",
    )

    list_filter = (
        "is_locked",
        "created_at",
    )

    ordering = (
        "-last_attempt",
    )

    readonly_fields = (
        "uuid",
        "created_at",
        "last_attempt",
    )

    list_per_page = 25

    date_hierarchy = "created_at"


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "uuid",
        "user",
        "action",
        "status",
        "ip_address",
        "browser",
        "operating_system",
        "device_type",
        "created_at",
    )

    list_display_links = (
        "uuid",
    )

    search_fields = (
        "user__email",
        "ip_address",
        "browser",
        "operating_system",
    )

    list_filter = (
        "action",
        "status",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "uuid",
        "user",
        "action",
        "status",
        "ip_address",
        "user_agent",
        "browser",
        "operating_system",
        "device_type",
        "endpoint",
        "created_at",
    )

    list_select_related = (
        "user",
    )

    list_per_page = 50

    date_hierarchy = "created_at"