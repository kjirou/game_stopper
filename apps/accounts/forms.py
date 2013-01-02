# coding: utf8
import re
from django import forms
from django.contrib.auth import login as auth_login, authenticate
from django.forms import widgets
from accounts.models import User, UserProfile


class UsernameField(forms.RegexField):

    def __init__(self):
        super(self.__class__, self).__init__(
            re.compile(r'^[-_.a-zA-Z0-9]+$'),
            min_length=4,
            max_length=16,
        )


class PasswordField(forms.RegexField):

    def __init__(self):
        super(self.__class__, self).__init__(
            re.compile(r'^[a-zA-Z0-9]+$'),
            min_length=4,
            max_length=16,
            widget=forms.PasswordInput()
        )


class SignUpForm(forms.Form):

    username = UsernameField()
    password = PasswordField()

    def clean(self):
        if self._errors:
            return

        # 後で：
        # usernameとemailの重複チェック
        # もしかしたら各々のフィールドに持たせた方がいいかも
        # 基本はTwitterからなので後回し

        return self.cleaned_data


class SignInForm(forms.Form):

    username = UsernameField()
    password = PasswordField()

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        if self._errors:
            return

        # FIXME:
        # - I want to replace error messages to Django's original messages
        # - If use a one custom message for two places,
        #     then that message must be managed by using constant etc

        username = self.data['username']
        password = self.data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('The user is not existed')
        elif user.get_profile() is None:
            raise forms.ValidationError('The user is not existed')
        elif user.is_active is False:
            raise forms.ValidationError('The user is not available')
        self._user = user

        return self.cleaned_data

    def get_user(self):
        return self._user
