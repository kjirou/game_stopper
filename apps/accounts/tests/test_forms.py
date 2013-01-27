# coding: utf-8
from django.test import TestCase, Client
from accounts.forms import ProfiledUserOnlyAuthenticationForm
from accounts.models import User, UserProfile


class ProfiledUserOnlyAuthenticationFormTest(TestCase):
    u'''ProfiledUserOnlyAuthenticationFormのテスト'''

    def _sign_up(self):
        return UserProfile.objects.sign_up(
            self._username, self._password)

    def setUp(self):
        self._username = 'testuser'
        self._password = 'testpw'

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_success(self):
        u'''ログイン成功'''
        self._sign_up()
        form = ProfiledUserOnlyAuthenticationForm(data={
            'username': self._username,
            'password': self._password,
        })
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_failures(self):
        u'''ログイン失敗各種'''
        self._sign_up()

        form = ProfiledUserOnlyAuthenticationForm(data={
            'username': 'notexisted',
            'password': self._password,
        })
        self.assertFalse(form.is_valid())

        form = ProfiledUserOnlyAuthenticationForm(data={
            'username': self._username,
            'password': 'notexisted',
        })
        self.assertFalse(form.is_valid())

        # UserProfile無しのユーザはログイン不可
        profileless_username = 'profileless'
        profileless_password = 'test'
        User.objects.create_user(
            profileless_username, password=profileless_password)
        form = ProfiledUserOnlyAuthenticationForm(data={
            'username': profileless_username,
            'password': profileless_password,
        })
        self.assertFalse(form.is_valid())
