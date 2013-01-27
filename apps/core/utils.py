# coding: utf-8
from django.conf import settings
import os
import shutil


def get_test_tmp_dir():
    return settings.TMP_ROOT + '/test'


def create_test_tmp_dir():
    path = get_test_tmp_dir()
    if not os.path.isdir(path):
        os.mkdir(path)


def delete_test_tmp_dir():
    path = get_test_tmp_dir()
    if os.path.isdir(path):
        shutil.rmtree(path)
