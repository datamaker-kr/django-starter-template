from django import forms
from django_select2.forms import Select2TagWidget


class DynamicArrayWidget(forms.TextInput):

    template_name = 'common/widgets/dynamic_array.html'

    class Media:
        js = [
            '/static/common/js/dynamic-array.js'
        ]

    def get_context(self, name, value, attrs):
        value = value or ['']
        context = super().get_context(name, value, attrs)
        final_attrs = context['widget']['attrs']
        id_ = context['widget']['attrs'].get('id')

        subwidgets = []
        for index, item in enumerate(context['widget']['value']):
            widget_attrs = final_attrs.copy()
            if id_:
                widget_attrs['id'] = '%s_%s' % (id_, index)
            widget = forms.TextInput()
            widget.is_required = self.is_required
            subwidgets.append(widget.get_context(name, item, widget_attrs)['widget'])

        context['widget']['subwidgets'] = subwidgets
        return context

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def format_value(self, value):
        return value or []


class ArrayFieldWidget(Select2TagWidget):

    def value_from_datadict(self, data, files, name):
        values = super(ArrayFieldWidget, self).value_from_datadict(data, files, name)
        return ",".join(values)

    def optgroups(self, name, value, attrs=None):
        if value:
            values = value[0].split(',') if value[0] else []
            selected = set(values)
            subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
            return [(None, subgroup, 0)]
        return [(None, [], 0)]
