# coding: utf8
from django.db import models
from accounts.models import UserProfile


class Twitterer(models.Model):
    user_profile = models.OneToOneField(UserProfile)
    twitter_id = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.twitter_id,)

    class Meta:
        db_table = 'twauthorizer_twitterer'
        verbose_name = 'Twitterer'
        verbose_name_plural = 'Twitterers'
