import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'test-key-for-testing-only'

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'messaging.apps.MessagingConfig',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'auth.User'

ROOT_URLCONF = 'messaging.urls'

TIME_ZONE = 'UTC'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
