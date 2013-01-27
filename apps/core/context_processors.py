# coding: utf-8
from django.conf import settings


def urls_and_paths(request):
    return {
        'MEDIA_URL': settings.MEDIA_URL,
    }
