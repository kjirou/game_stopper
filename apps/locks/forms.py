# coding: utf-8
from django.conf import settings
import re
from django import forms
from django.forms import widgets


class LockedFileField(forms.FileField):

    def __init__(self):
        super(self.__class__, self).__init__()
        self._max_file_size = settings.MAX_LOCKED_FILE_SIZE
        self._max_file_name_length = settings.MAX_LOCKED_FILE_NAME_LENGTH

    def clean(self, value, initial):
        if value is None:
            raise forms.ValidationError('Empty file')

        if value.size > self._max_file_size:
            raise forms.ValidationError('Over file size')
        if len(value.name) > self._max_file_name_length:
            raise forms.ValidationError('Over file name length')

        return value


class CreateForm(forms.Form):

    locked_file = LockedFileField()
    period = forms.IntegerField(
        min_value=1, max_value=30, initial=7)
    saved_hours = forms.IntegerField(
        min_value=1, max_value=30 * 24, initial=7)

    #def clean(self):
    #    if self._errors:
    #        return

    #    # TODO:
    #    # - 最大save_hoursは日数 * 24で切り捨てる

    #    return self.cleaned_data
