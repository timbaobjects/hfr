from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=100)


class FormGroup(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, related_name='groups')


class FormField(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=255, blank=True)
    represents_boolean = models.BooleanField(default=False)
    group = models.ForeignKey(FormGroup, related_name='fields')
