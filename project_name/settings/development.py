from .base import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'secret'

DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ project_name }}',
        'USER': 'postgres',
        'ATOMIC_REQUESTS': True
    }
}
