# coding: utf8
import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
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


class ProfiledUserOnlyAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
            # Mod
            try:
                self.user_cache.get_profile()
            except UserProfile.DoesNotExist:
                raise forms.ValidationError(self.error_messages['inactive'])
            # /Mod
        self.check_for_test_cookie()
        return self.cleaned_data
