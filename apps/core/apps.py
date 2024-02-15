from django.apps import AppConfig

from .patches import patch_thumbnail_storage

# FIXME: easy_thumbnail의 storage 설정방식이 django 4.2 이후의 storage 설정방식을 지원하지 않은 관계로 workaround 진행
patch_thumbnail_storage()


class CoreAppConfig(AppConfig):
    name = 'apps.core'
