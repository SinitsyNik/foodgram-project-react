from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    empty_value_display = '-пусто-'
