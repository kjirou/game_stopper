# coding: utf8
from django.conf import settings
import re
import datetime
from django.core.files import File
from django.utils.crypto import get_random_string
from django.utils.timezone import now as django_now
from django.db import models
from accounts.models import UserProfile
from locks.filelocker import FileLocker


class LockManager(models.Manager):

    def create_by_user(self, user, uploaded_file, period, saved_hours):
        locked_at = django_now()
        unlockable_at = locked_at + datetime.timedelta(days=period)

        max_saved_hours = period * 24
        if saved_hours > max_saved_hours:
            saved_hours = max_saved_hours

        password = get_random_string(8, allowed_chars='0123456789')
        fl = FileLocker()
        fl.lock(uploaded_file, password)
        locked_file = File(
            open(fl.get_locked_file_path(), 'r'),
            name=fl.get_locked_file_name()
        )

        obj = self.create(
            user_profile=user.get_profile(),
            locked_file=locked_file,
            locked_file_name=fl.get_locked_file_name(),
            original_file_name=uploaded_file.name,
            original_file_size=uploaded_file.size,
            password=password,
            locked_at=locked_at,
            unlockable_at=unlockable_at,
            saved_hours=saved_hours
        )

        locked_file.close()
        fl.clean()
        return obj


def _locked_file_upload_to(instance, filename):
    now = django_now()
    return '%s/%04d/%02d/%s/%s' % (
        settings.LOCKED_FILES_DIR_NAME,
        now.year,
        now.month,
        get_random_string(32),
        filename,
    )


class Lock(models.Model):
    objects = LockManager()
    user_profile = models.ForeignKey(UserProfile, related_name='lock_set')
    locked_file = models.FileField(upload_to=_locked_file_upload_to)
    locked_file_name = models.CharField(max_length=255)
    original_file_name = models.CharField(max_length=255)
    original_file_size = models.PositiveIntegerField()
    password = models.CharField(max_length=16)
    locked_at = models.DateTimeField(help_text=u'施錠日時')
    unlockable_at = models.DateTimeField(help_text=u'解錠可能日時')
    unlocked_at = models.DateTimeField(
        blank=True, null=True, help_text=u'解錠日時')
    saved_hours = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' % (self.original_file_name,)

    class Meta:
        db_table = 'locks_lock'
        verbose_name = 'Lock'
        verbose_name_plural = 'Locks'
