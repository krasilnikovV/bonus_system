import os
from .settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

ALLOWED_HOSTS = []  # Add your hosts

DEBUG = False

# DB Settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NameOfDB',
        'USER': 'login',
        'PASSWORD': 'password',
        'HOST': '172.**.**.58',
        'PORT': '80',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')