from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser()
    list_display = ('username', 'email', 'is_main_admin', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_main_admin',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
