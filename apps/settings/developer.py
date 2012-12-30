from settings.base import *

ADMINS = (
    ('Your name', 'your@email.address'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR + '/game_stopper.sqlite',
    }
}
