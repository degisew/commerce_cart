from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from commerce_cart.account.forms import UserChangeForm, UserCreationForm
from commerce_cart.account.models import Role, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ["email", "is_staff", "role"]
    list_filter = ["is_staff", "role"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Permissions",
            {"fields": ["is_staff", "role"]},
        ),
        ("Important dates", {"fields": ["created_at", "updated_at", "deleted_at"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "role",
                ],
            },
        )
    ]

    search_fields = ["email"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = []


admin.site.register(Role)

# We don't need Group
admin.site.unregister(Group)
