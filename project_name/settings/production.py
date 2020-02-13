from .base import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'secret'

DEBUG = False


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': '{{ project_name }}',
        'USER': '{{ project_name }}',
        'PASSWORD': '',
        'ATOMIC_REQUESTS': True
    }
}


# Security

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
