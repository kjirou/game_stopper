# coding: utf-8
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase
from locks.forms import CreateForm
from locks.models import Lock


class CreateFormTest(TestCase):
    u'''CreateFormのテスト'''

    def _create_files_for_locked_file(self, name='dummy.txt', size=1024*1024):
        # 日本語を含むファイル名を普通にアップした場合、
        # request.FILES['field_name'].name はUnicode型になっている
        uploaded_file = SimpleUploadedFile(name, '0' * size)
        return {
            'locked_file': uploaded_file,
        }

    def test_normal(self):
        u'''正しい入力'''
        files = self._create_files_for_locked_file()
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertTrue(form.is_valid())

    def test_file_size(self):
        u'''ファイルサイズチェックの確認'''
        # 上限一杯
        files = self._create_files_for_locked_file(size=settings.MAX_LOCKED_FILE_SIZE)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertTrue(form.is_valid())
        # 上限オーバー
        files = self._create_files_for_locked_file(size=settings.MAX_LOCKED_FILE_SIZE + 1)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertFalse(form.is_valid())

    def test_multibyte_file_name(self):
        u'''マルチバイトファイル名の確認'''
        file_name = u'ダミー'
        files = self._create_files_for_locked_file(name=file_name)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertTrue(form.is_valid())

    def test_file_name_length(self):
        u'''ファイル名長チェックの確認'''
        # 上限一杯
        file_name = 'a' * (settings.MAX_LOCKED_FILE_NAME_LENGTH - 4) + '.exe'
        files = self._create_files_for_locked_file(name=file_name)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertTrue(form.is_valid())
        # 上限オーバー
        file_name = 'a' * (settings.MAX_LOCKED_FILE_NAME_LENGTH - 3) + '.exe'
        files = self._create_files_for_locked_file(name=file_name)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertFalse(form.is_valid())
        # マルチバイト上限一杯
        file_name = u'あ' * (settings.MAX_LOCKED_FILE_NAME_LENGTH - 4) + '.exe'
        files = self._create_files_for_locked_file(name=file_name)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertTrue(form.is_valid())
        # マルチバイト上限オーバー
        file_name = u'あ' * (settings.MAX_LOCKED_FILE_NAME_LENGTH - 3) + '.exe'
        files = self._create_files_for_locked_file(name=file_name)
        form = CreateForm({
            'period': '7',
            'saved_hours': '7',
        }, files)
        self.assertFalse(form.is_valid())
