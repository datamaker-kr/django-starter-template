import os
import uuid

from django.db.models import Q
from django.utils.deconstruct import deconstructible


@deconstructible
class FilenameChanger(object):

    def __init__(self, base_path, ext=None):
        self.base_path = base_path
        self.ext = ext

    def __call__(self, instance, filename, *args, **kwargs):
        splits = filename.split('.')
        if len(splits) > 1:
            ext = splits[-1].lower()
        else:
            ext = self.ext
        filename = "%s.%s" % (uuid.uuid4(), ext)

        return os.path.join(self.base_path, filename)

    def __eq__(self, other):
        return self.base_path


@deconstructible
class LimitTagChoices(object):

    def __init__(self, model):
        self.model = model

    def __call__(self):
        return Q(content_type__model=self.model) | Q(content_type__isnull=True)


def has_changed(instance, fields):
    model = instance._meta.model
    created = not instance.pk

    if created:
        return True

    else:
        has_changed = False
        instance_old = model.objects.get(id=instance.pk)

        for field in fields:
            has_changed = getattr(instance, field) != getattr(instance_old, field)
            if has_changed:
                break

        return has_changed
