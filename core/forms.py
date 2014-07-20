from django import forms
from form_utils import forms as better_forms
from checklists.models import Form


class ReportEditFormBase(better_forms.BetterForm):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        form = self.instance.form if self.instance.form else Form.objects.first()
        kwargs['initial'].update({
            'data__{}'.format(tag): self.instance.data.get(tag)
            for tag in form.tags
        })

        return super(ReportEditFormBase, self).__init__(*args, **kwargs)

    def save(self):
        data = {k.replace('data__', ''): v
                for k, v in self.cleaned_data.iteritems()
                if k.startswith('data__')
                }

        # weed out unused keys
        keys = data.keys()
        for key in keys:
            if data[key] in ('', False, None):
                data.pop(key)

        self.instance.data = data
        return self.instance.save()


def generate_report_edit_form(form):
    fields = {}
    groups = []

    for group in form.groups.all():
        groupspec = (group.name, {'fields': [], 'legend': group.name})
        for field in group.fields.all():
            field_name = 'data__{}'.format(field.name)
            groupspec[1]['fields'].append(field_name)

            options = list(field.options.all())
            if options:
                choices = [('', 'None')] + \
                    [(option.value, option.label) for option in options]

                fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    help_text=field.description,
                    label=field.name,
                    required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-1'}))
            else:
                fields[field_name] = forms.IntegerField(
                    help_text=field.description,
                    label=field.name,
                    required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-1'}))

        groups.append(groupspec)

    metaclass = type('Meta', (), {'fieldsets': groups})
    fields['Meta'] = metaclass

    return type('ReportEditForm', (ReportEditFormBase,), fields)
