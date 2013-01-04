from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class UserProfileManager(models.Manager):

    def sign_up(self, username, password):
        User.objects.create_user(username, password=password)
        user = authenticate(username=username, password=password)
        return self.create(user=user)


class UserProfile(models.Model):
    objects = UserProfileManager()
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'%s:u%s:%s' % (self.id, self.user.id, self.user.username)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
