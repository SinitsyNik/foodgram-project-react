from django.contrib import admin
from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_filter = ('user')
    empty_value_display = '-пусто-'


admin.site.register(Follow)
