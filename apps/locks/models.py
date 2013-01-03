# coding: utf8
from django.db import models
from accounts.models import UserProfile


class Lock(models.Model):
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
