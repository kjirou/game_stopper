# coding: utf8
from django.conf import settings


def file_infos(request):
    return {
        'MAX_LOCKED_FILE_SIZE': settings.MAX_LOCKED_FILE_SIZE,
    }
