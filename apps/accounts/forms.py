# coding: utf8
import re
from django import forms
from django.forms import widgets
from accounts import models


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

        # usernameとemailの重複チェック
        # もしかしたら各々のフィールドに持たせた方がいいかも
        # 基本はTwitterからなので後回し

        return self.cleaned_data


class SignInForm(forms.Form):

    username = UsernameField()
    password = PasswordField()

    def clean(self):
        if self._errors:
            return

        # ログイン処理？

        return self.cleaned_data
