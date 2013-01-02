# coding: utf8
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from accounts.models import User, UserProfile


class SignUpViewTest(TestCase):
    u'''sign_upビューのテスト'''

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_complete_signed_up(self):
        u'''登録完了'''
        c = Client()
        username = 'testuser'
        response = c.post(reverse('accounts:sign_up'), {
            'username': username,
            'password': 'testpw',
        })
        UserProfile.objects.get(user__username=username)
        self.assertEqual(UserProfile.objects.all().count(), 1)
