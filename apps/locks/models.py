# coding: utf8
import datetime
from django.contrib.auth.models import User
from django.db import models
from accounts.models import UserProfile


class LockManager(models.Manager):

    def create_by_user(self, user_profile, uploaded_file, period, saved_hours):
        locked_at = datetime.datetime.now()
        unlockable_at = locked_at + datetime.timedelta(days=period)

        max_saved_hours = period * 24
        if saved_hours > max_saved_hours:
            saved_hours = max_saved_hours

        return self.create(
            user_profile=user_profile,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            password=User.objects.make_random_password(8),
            locked_at=locked_at,
            unlockable_at=unlockable_at,
            saved_hours=saved_hours
        )


class Lock(models.Model):
    objects = LockManager()
    user_profile = models.ForeignKey(UserProfile, related_name='lock_set')
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
