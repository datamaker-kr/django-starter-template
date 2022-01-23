import os
import uuid

from django.db.models import Q
from django.utils.deconstruct import deconstructible


@deconstructible
class UUIDUploader(object):
    base_path = None
    ext = None
    shard = None

    def __init__(self, base_path, ext=None, shard=None):
        self.base_path = base_path
        self.ext = ext
        self.shard = shard

    def __call__(self, instance, filename, *args, **kwargs):
        base_path = self.base_path.format(instance=instance, filename=filename)

        splits = filename.split('.')
        if len(splits) > 1:
            ext = splits[-1].lower()
        else:
            ext = self.ext

        if ext:
            filename = f'{uuid.uuid4()}.{ext}'
        else:
            filename = f'{uuid.uuid4()}'

        if self.shard:
            paths = self.get_sharded_paths(filename)
        else:
            paths = [filename]
        return os.path.join(base_path, *paths)

    def __eq__(self, other):
        return self.base_path

    def get_sharded_paths(self, string, rest_only=False):
        width = self.shard[0]
        depth = self.shard[1]

        for i in range(depth):
            yield string[(width * i):(width * (i + 1))]

        if rest_only:
            yield string[(width * depth):]
        else:
            yield string
