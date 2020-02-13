from django.conf import settings
from django.contrib.sites.models import Site


def get_host():
    domain = Site.objects.get_current().domain
    return 'http://{}'.format(domain)


def get_absolute_url(url):
    return '{}{}'.format(settings.BASE_URL, url)
