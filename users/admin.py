from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "verification_code",
        "invite_code",
        "invited_by",
    )
