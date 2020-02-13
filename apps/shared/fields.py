from functools import partialmethod
from itertools import chain

from django import forms
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.utils import prefix_validation_error
from django.db.models import CharField

from .widgets import DynamicArrayWidget


def get_field_display_list(self, field):
    values = getattr(self, field.attname)
    if values:
        choice_dict = dict(field.base_field.flatchoices)
        return [choice_dict.get(value, value) for value in values]
    return []


def get_field_display(self, field):
    values = getattr(self, field.attname)
    if values:
        choice_dict = dict(field.base_field.flatchoices)
        return ', '.join([choice_dict.get(value, value) for value in values])
    return ''


class ArraySelectMultiple(forms.CheckboxSelectMultiple):

    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
            'widget': ArraySelectMultiple
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)

    def contribute_to_class(self, cls, name, private_only=False):
        super(ArrayField, self).contribute_to_class(cls, name, private_only)
        setattr(cls, 'get_%s_display_list' % self.name, partialmethod(get_field_display_list, field=self))
        setattr(cls, 'get_%s_display' % self.name, partialmethod(get_field_display, field=self))


class DynamicArrayField(forms.Field):

    default_error_messages = {
        'item_invalid': 'Item %(nth)s in the array did not validate: ',
    }

    def __init__(self, base_field, **kwargs):
        self.base_field = base_field
        self.max_length = kwargs.pop('max_length', None)
        kwargs.setdefault('widget', DynamicArrayWidget)
        super().__init__(**kwargs)

    def clean(self, value):
        cleaned_data = []
        errors = []
        value = filter(None, value)
        for index, item in enumerate(value):
            try:
                cleaned_data.append(self.base_field.clean(item))
            except forms.ValidationError as error:
                errors.append(prefix_validation_error(
                    error, self.error_messages['item_invalid'],
                    code='item_invalid', params={'nth': index},
                ))
        if errors:
            raise forms.ValidationError(list(chain.from_iterable(errors)))
        if cleaned_data and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return cleaned_data


class AutoURLField(CharField):
    default_validators = []
    description = 'URL'

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs.setdefault('max_length', 200)
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 200:
            del kwargs['max_length']
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        value = forms.URLField().to_python(value)
        setattr(model_instance, self.attname, value)
        return value
