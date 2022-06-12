from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from user.models import User, Volunteer, Employer


class MyUserAdmin(UserAdmin):
    fieldsets = (
        ('Конфиденциальная информация', {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'telegram_id', 'avatar')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('email',)
    list_display = ['first_name', 'last_name', 'email', 'telegram_id', 'avatar']


admin.site.register(User, MyUserAdmin)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    pass
