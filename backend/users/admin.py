from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'telegram_id',]
    search_fields = ['username', 'telegram_id',]

    readonly_fields = ['telegram_id',]
