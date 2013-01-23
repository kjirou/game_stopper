# coding: utf8
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from accounts.models import User, UserProfile


class SignUpViewTest(TestCase):
    u'''sign_upビューのテスト'''

    def _sign_up(self):
        return UserProfile.objects.sign_up(
            self._username, self._password)

    def setUp(self):
        self._username = 'testuser'
        self._password = 'testpw'

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    #def test_complete_signed_up(self):
    #    u'''登録完了'''
    #    username = 'testuser'
    #    response = self.client.post(reverse('accounts:sign_up'), {
    #        'username': username,
    #        'password': 'testpw',
    #    })
    #    UserProfile.objects.get(user__username=username)
    #    self.assertEqual(UserProfile.objects.all().count(), 1)

    # マイページなどのログインが必要なページを開いて
    # status_codeで判別するらしい、のでその後でやる
    # - client.loginを使ってもいいらしい
    #def test_success_signed_in(self):
    #    u'''ログイン成功'''
    #    user_profile = self._sign_up()
    #
    #    response = self.client.post(reverse('accounts:sign_in'), {
    #        'username': self._username,
    #        'password': self._password,
    #    })
    #
    #    print dir(self.client)
    #    #self.assertTrue(response.request.user.is_authenticated())
