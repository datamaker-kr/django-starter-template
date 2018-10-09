from .base import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'secret'

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ project_name }}',
        'USER': 'postgres',
        'ATOMIC_REQUESTS': True
    }
}
