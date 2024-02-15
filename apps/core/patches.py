from django.core.files.storage import storages


def patch_thumbnail_storage():
    from easy_thumbnails import storage

    storage.thumbnail_default_storage = storages['default']
