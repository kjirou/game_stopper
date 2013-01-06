# coding: utf8
from django.conf import settings
import os
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import is_aware
from core.utils import get_test_tmp_dir, create_test_tmp_dir, \
    delete_test_tmp_dir
from accounts.models import UserProfile
from locks.models import Lock


class LockTest(TestCase):
    u'''Lockモデルのテスト'''

    def _create_user_profile(self):
        return UserProfile.objects.sign_up(
            self._username, self._password)

    def setUp(self):
        self._username = 'testuser'
        self._password = 'testpw'
        create_test_tmp_dir()

    def tearDown(self):
        Lock.objects.all().delete()
        delete_test_tmp_dir()

    @override_settings(MEDIA_ROOT=get_test_tmp_dir())
    def test_normal_creation(self):
        u'''正常な登録処理を確認、以下のケースも含める
        - 救済時間の 期間 * 24時間 を上限とした切り捨て処理
        - awareなUTC時間で保存されているか
        - FieldFileの操作、使ったことないから
          https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.fields.files.FieldFile
        '''
        user_profile = self._create_user_profile()
        file_name = 'dummy.txt'
        size = 1024 * 1024
        uploaded_file = SimpleUploadedFile(file_name, '0' * size)
        period = 10
        saved_hours = 999999

        Lock.objects.create_by_user(
            user_profile.user,
            uploaded_file,
            period,
            saved_hours
        )

        lock_obj = Lock.objects.get(original_file_name=file_name)
        # 救済時間が正しく切り捨てられているか
        self.assertEqual(lock_obj.saved_hours, period * 24)
        # UTC時間か
        self.assertTrue(is_aware(lock_obj.locked_at))
        # ファイルが正しく保存されているか
        self.assertTrue(bool(lock_obj.locked_file))
        # サイズが正しいか、圧縮後のサイズは不明なので0超で確認
        self.assertNotEqual(len(lock_obj.locked_file.read()), 0)
        # ファイル削除
        locked_file_path = lock_obj.locked_file.path  # ファイルまでの絶対パス
        self.assertTrue(os.path.isfile(locked_file_path))
        lock_obj.locked_file.delete()
        self.assertFalse(os.path.isfile(locked_file_path))
        self.assertFalse(bool(lock_obj.locked_file))
