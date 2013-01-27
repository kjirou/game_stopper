# coding: utf-8
from django.contrib import admin
from twauthorizer.models import Twitterer


class TwittererAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__']
    list_display_links = ['id', '__unicode__']
    raw_id_fields = ('user_profile',)
    save_on_top = True
    actions = None
admin.site.register(Twitterer, TwittererAdmin)
