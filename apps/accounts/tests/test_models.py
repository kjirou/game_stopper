# coding: utf-8
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

    def test_sign_up(self):
        u'''sign_upメソッドの確認'''
        username = 'testuser'
        password = 'testpw'
        user_profile = UserProfile.objects.sign_up(username, password)
        # DBに存在するか
        UserProfile.objects.get(user__username=username)
