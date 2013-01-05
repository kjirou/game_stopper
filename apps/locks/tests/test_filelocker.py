# coding: utf8
from django.conf import settings
import os
import zipfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from core.utils import get_test_tmp_dir, create_test_tmp_dir, \
    delete_test_tmp_dir
from locks.filelocker import FileLocker


class FileLockerTest(TestCase):
    u'''filelockerモジュールのテスト'''

    def setUp(self):
        create_test_tmp_dir()

    def tearDown(self):
        delete_test_tmp_dir()

    def test_create_container_name(self):
        u'''_create_container_nameのテスト'''
        fl = FileLocker()
        self.assertRegexpMatches(
            fl._create_container_name(), r'gs-locked-\d+')

    def test_copy(self):
        u'''_copyのテスト'''
        file_name = 'dummy.txt'
        size = 1024 * 1024 * 5  # chunksテストのために2.5MB以上にする
        content = 'a' * size
        uploaded_file = SimpleUploadedFile(file_name, content)
        path = get_test_tmp_dir() + '/' + file_name

        FileLocker()._copy(uploaded_file, path)
        # 保存したファイルを開けて内容が一致するかを確認
        fh = open(path, 'r')
        self.assertEqual(content, fh.read())

    @override_settings(FILELOCKER_WORKING_ROOT=get_test_tmp_dir())
    def test_lock_and_delete(self):
        u'''lockとdeleteのテスト'''
        file_name = 'dummy.txt'
        size = 1024 * 1024
        content = 'a' * size
        uploaded_file = SimpleUploadedFile(file_name, content)
        password = 'abcd1234'

        fl = FileLocker()
        fl.lock(uploaded_file, password)
        locked_file_path = fl.get_locked_file_path()

        # ファイルが存在し、zip形式か
        self.assertTrue(zipfile.is_zipfile(locked_file_path))
        # パスワード無しで解凍できないか
        zip = zipfile.ZipFile(locked_file_path, 'r')
        try:
            zip.testzip()
            self.fail('zip file is not encrypted')
        except RuntimeError:
            pass
        # パスワード付きで解凍できるか
        zip.setpassword(password)
        zip.testzip()
        # 正しいファイル名で格納されているか
        self.assertEqual(zip.namelist()[0], file_name)
        # ファイルの内容は正しいか
        fh = zip.open(file_name, 'r')
        self.assertEqual(fh.read(), content)
        fh.close()
        zip.close()
        # 一時ファイル群の削除と確認
        self.assertTrue(os.path.isdir(fl._working_dir_path))
        fl.delete()
        self.assertFalse(os.path.isdir(fl._working_dir_path))
