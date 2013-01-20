# coding: utf8
import tweepy
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest


VERIFIED_TWITTER_ID_SESSION_KEY = 'twauthorizer_verified_twitter_id'
REQUEST_TOKEN_SESSION_KEY = 'twauthorizer_request_token'


def auth(request):
    u'''Twitter OAuth Authentication

    Ref)
    http://spiri-tua-lism.com/?p=200
    https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
    '''
    auth = tweepy.OAuthHandler(
        settings.TWAUTHORIZER_CONSUMER_KEY,
        settings.TWAUTHORIZER_CONSUMER_SECRET,
        request.build_absolute_uri(reverse('twauthorizer:auth_callback'))
    )
    auth_url = auth.get_authorization_url()
    request.session[REQUEST_TOKEN_SESSION_KEY] = \
        (auth.request_token.key, auth.request_token.secret)
    return HttpResponseRedirect(auth_url)


def auth_callback(request):

    verifier = request.GET.get('oauth_verifier', '')
    token = request.session.get(REQUEST_TOKEN_SESSION_KEY, ('', ''))
    del request.session[REQUEST_TOKEN_SESSION_KEY]

    auth = tweepy.OAuthHandler(
        settings.TWAUTHORIZER_CONSUMER_KEY,
        settings.TWAUTHORIZER_CONSUMER_SECRET
    )

    auth.set_request_token(*token)
    try:
        # This is not existed in <https://github.com/tweepy/tweepy/blob/master/examples/oauth.py>.
        # But it is need.
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return HttpResponseRedirect(settings.LOGIN_URL)

    api = tweepy.API(auth)
    request.session[VERIFIED_TWITTER_ID_SESSION_KEY] = api.me().id_str

    return HttpResponse('auth_callback')
