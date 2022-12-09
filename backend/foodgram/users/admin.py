from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    search_fields = ('username',)
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'
