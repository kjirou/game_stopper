from django.db import models
from django.contrib.auth.models import User


class UserProfileManager(models.Manager):

    def create_with_user(self, username, password):
        user = User.objects.create_user(username, password=password)
        obj = self.create(user=user)
        return obj


class UserProfile(models.Model):
    objects = UserProfileManager()
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'%s:u%s:%s' % (self.id, self.user.id, self.user.username)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
