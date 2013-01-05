# coding: utf8
from django.conf import settings
import os
import subprocess
from django.utils.crypto import get_random_string
from django.utils.timezone import now as django_now


def _create_working_dir_path():
    return '%s/%s' % (
        settings.FILELOCKER_WORKING_ROOT,
        get_random_string(32),
    )


def _create_zipped_dir_name():
    return django_now().strftime('gs-locked-%Y%m%d%H%M%S')


def _copy(uploaded_file, file_path):
    fh = open(file_path, 'w')
    for chunk in uploaded_file.chunks():
        fh.write(chunk)
    fh.close()


def _to_zip(zip_file_path, zipped_dir_path, password):
    subprocess.check_output([
        'zip',
        '-r',
        '-j',
        '-P' + password,
        zip_file_path,
        zipped_dir_path,
    ])


def lock(uploaded_file, password):
    working_dir_path = _create_working_dir_path()
    zipped_dir_name = _create_zipped_dir_name()
    zipped_dir_path = working_dir_path + '/' + zipped_dir_name
    zip_file_path = zipped_dir_path + '.zip'

    os.makedirs(zipped_dir_path)
    _copy(uploaded_file, zipped_dir_path + '/' + uploaded_file.name)
    _to_zip(zip_file_path, zipped_dir_path, password)

    return zip_file_path


def delete():
    pass
