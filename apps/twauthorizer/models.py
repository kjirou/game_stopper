from django.db import models
from django.utils.crypto import get_random_string
from accounts.models import UserProfile


class TwittererManager(models.Manager):

    def sign_up(self, twitter_id, screen_name):
        user_profile = UserProfile.objects.sign_up(
            screen_name, get_random_string(16))
        return self.create(
            user_profile=user_profile,
            twitter_id=twitter_id,
            screen_name=screen_name
        )


class Twitterer(models.Model):
    objects = TwittererManager()
    user_profile = models.OneToOneField(UserProfile)
    twitter_id = models.CharField(max_length=255, unique=True)
    screen_name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.twitter_id,)

    class Meta:
        db_table = 'twauthorizer_twitterer'
        verbose_name = 'Twitterer'
        verbose_name_plural = 'Twitterers'
