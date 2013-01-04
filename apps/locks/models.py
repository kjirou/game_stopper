# coding: utf8
from django.conf import settings
import datetime
from django.utils.timezone import now as use_tz_now
from django.contrib.auth.models import User
from django.db import models
from accounts.models import UserProfile


class LockManager(models.Manager):

    def create_by_user(self, user, uploaded_file, period, saved_hours):
        locked_at = use_tz_now()
        unlockable_at = locked_at + datetime.timedelta(days=period)

        max_saved_hours = period * 24
        if saved_hours > max_saved_hours:
            saved_hours = max_saved_hours

        return self.create(
            user_profile=user.get_profile(),
            locked_file=uploaded_file,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            password=User.objects.make_random_password(8),
            locked_at=locked_at,
            unlockable_at=unlockable_at,
            saved_hours=saved_hours
        )


def _locked_file_upload_to(instance, filename):
    return '%s%s/%s' % (
        settings.MEDIA_ROOT,
        settings.LOCKED_FILES_DIR_NAME,
        User.objects.make_random_password(32),
    )


class Lock(models.Model):
    objects = LockManager()
    user_profile = models.ForeignKey(UserProfile, related_name='lock_set')
    locked_file = models.FileField(
        upload_to=_locked_file_upload_to, blank=True, null=True)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    password = models.CharField(max_length=16)
    locked_at = models.DateTimeField(help_text=u'施錠日時')
    unlockable_at = models.DateTimeField(help_text=u'解錠可能日時')
    unlocked_at = models.DateTimeField(
        blank=True, null=True, help_text=u'解錠日時')
    saved_hours = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' % (self.file_name,)

    class Meta:
        db_table = 'locks_lock'
        verbose_name = 'Lock'
        verbose_name_plural = 'Locks'
