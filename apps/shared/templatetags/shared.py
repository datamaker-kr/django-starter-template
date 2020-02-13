from django import template

from apps.shared.utils.network import get_absolute_url

register = template.Library()


@register.filter(name='absolute_url')
def get_absolute_url_(url):
    return get_absolute_url(url)
