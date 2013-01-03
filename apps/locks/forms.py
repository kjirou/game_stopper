# coding: utf8
import re
from django import forms
from django.forms import widgets


class LockedFileField(forms.FileField):

    def __init__(self):
        super(self.__class__, self).__init__()
        self._max_file_size = 1024 * 100
        self._file_data = None
        self._file_size = None
        self._file_name = None

    def clean(self, value, initial):
        if value is None:
            raise forms.ValidationError('Empty file')

        self._file_data = value.read()
        value.seek(0)
        self._file_size = len(self._file_data)
        self._file_name = value.name

        if self._file_size > self._max_file_size:
            raise forms.ValidationError('Over file size')

        # TODO:
        # - ファイル名長過ぎチェック

        return value


class CreateForm(forms.Form):

    locked_file = LockedFileField()
    period = forms.IntegerField(
        min_value=1, max_value=30, initial=7)
    saved_hours = forms.IntegerField(
        min_value=1, max_value=30 * 24, initial=7)

    def clean(self):
        if self._errors:
            return

        # TODO:
        # - 最大save_hoursは日数 * 24で切り捨てる

        return self.cleaned_data
