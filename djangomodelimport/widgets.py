import operator

from django import forms


class CompositeLookupWidget(forms.Widget):
    def __init__(self, source, *args, **kwargs):
        self.source = source
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        getter = operator.itemgetter(*self.source)
        try:
            return getter(data)
        except KeyError:
            pass

    def value_omitted_from_data(self, data, files, name):
        for field_name in self.source:
            if field_name not in data:
                return True
        return False


class JSONFieldWidget(forms.Widget):
    template_name = 'django/forms/widgets/textarea.html'

    def render(self, name, value, attrs=None, renderer=None):
        return ''

    def value_omitted_from_data(self, data, files, name):
        return not any([key.startswith(name) for key in data.keys()])

    def value_from_datadict(self, data, files, name):
        extra_fields = {}
        for f in data.keys():
            if f.startswith(name):
                new_field = f[len(name) + 1:]
                extra_fields[new_field] = data[f]
        return extra_fields
