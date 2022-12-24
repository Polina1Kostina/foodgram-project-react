from django.contrib import admin
from .models import User, Subscription


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
    list_filter = ('email', 'username')
    list_editable = ('username',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'subscription',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    list_editable = ('user',)
    empty_value_display = '-пусто-'
