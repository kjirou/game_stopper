# coding: utf8
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import is_aware
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

    def tearDown(self):
        Lock.objects.all().delete()

    def test_normal_creation(self):
        u'''正常な登録処理を確認、以下のケースも含める
        - 救済時間の 期間 * 24時間 を上限とした切り捨て処理
        - awareなUTC時間で保存されているか
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

        lock = Lock.objects.get(file_name=file_name)
        # 救済時間が正しく切り捨てられているか
        self.assertEqual(lock.saved_hours, period * 24)
        # UTC時間か
        self.assertTrue(is_aware(lock.locked_at))
