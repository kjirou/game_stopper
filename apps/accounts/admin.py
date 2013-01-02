# coding: utf8
from django.contrib import admin
from django.core.urlresolvers import reverse
from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__', 'subactions']
    list_display_links = ['id', '__unicode__']
    raw_id_fields = ('user',)
    save_on_top = True
    actions = None

    def subactions(self, obj):
        return u'''<a href="%s">Change User</a>''' % (
            reverse('admin:auth_user_change', args=(obj.user.id,)),
        )
    subactions.allow_tags = True
    subactions.short_description = u'操作'
admin.site.register(UserProfile, UserProfileAdmin)
