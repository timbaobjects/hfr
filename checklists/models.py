from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    @property
    def tags(self):
        return FormField.objects.filter(group__form=self).values_list(
            'name', flat=True)


class FormGroup(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, related_name='groups')

    def __unicode__(self):
        return self.name

    @property
    def tags(self):
        return self.fields.values_list('name', flat=True)


class FormField(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=255, blank=True)
    represents_boolean = models.BooleanField(default=False)
    group = models.ForeignKey(FormGroup, related_name='fields')

    def __unicode__(self):
        return self.name


class FieldOption(models.Model):
    label = models.CharField(max_length=100)
    value = models.IntegerField()
    field = models.ForeignKey(FormField, related_name='options')

    def __unicode__(self):
        return '{}-{}'.format(self.label, self.value)
