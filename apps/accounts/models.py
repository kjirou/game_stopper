from django.db import models
from django.contrib.auth.models import User, UserManager


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'%s:u%s:%s' % (self.id, self.user.id, self.user.email)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
