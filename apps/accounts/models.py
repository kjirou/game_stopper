from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='user_profile_set')

    def __unicode__(self):
        return u'%s:u%s:%s' % (self.id, self.user.id, self.user.email)

    class Meta:
        db_table = 'user_manager_user_profile'
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
