# coding: utf8
from django.test import TestCase
from accounts.models import User, UserProfile


class UserProfileTest(TestCase):
    u'''UserProfileモデルのテスト'''

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_auth_profile_module(self):
        u'''AUTH_PROFILE_MODULE設定確認'''
        user = User.objects.create_user('test_user')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(user_profile, user.get_profile())
