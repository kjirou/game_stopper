from django.contrib.auth.models import User
from twauthorizer.models import Twitterer


class TwitterIdBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            twitterer = Twitterer.objects.get(twitter_id=username)
            return twitterer.user_profile.user
        except Twitterer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
