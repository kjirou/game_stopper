# coding: utf8
from django.contrib import admin
from locks.models import Lock


class LockAdmin(admin.ModelAdmin):
    list_display = [
        'id', '__unicode__', 'user_profile', 'file_size',
        'locked_at', 'unlockable_at', 'unlocked_at'
    ]
    list_display_links = ['id', '__unicode__']
    raw_id_fields = ('user_profile',)
    save_on_top = True
    actions = None
admin.site.register(Lock, LockAdmin)
