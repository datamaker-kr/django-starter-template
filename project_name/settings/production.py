from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = False


# Security

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
