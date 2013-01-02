# coding: utf8
from django.test import TestCase, Client
from accounts.forms import SignInForm
from accounts.models import User, UserProfile


class SignInFormTest(TestCase):
    u'''SignInFormのテスト'''

    def _create_user_profile(self):
        return UserProfile.objects.create_with_user(
            self._username, self._password)

    def setUp(self):
        self._username = 'testuser'
        self._password = 'testpw'

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_success(self):
        u'''ログイン成功'''
        user_profile = self._create_user_profile()
        form = SignInForm({
            'username': self._username,
            'password': self._password,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), user_profile.user)

    def test_failures(self):
        u'''複数のログイン失敗ケース'''
        self._create_user_profile()

        form = SignInForm({
            'username': 'notexisted',
            'password': self._password,
        })
        self.assertFalse(form.is_valid())

        form = SignInForm({
            'username': self._username,
            'password': 'notexisted',
        })
        self.assertFalse(form.is_valid())
