from checklists.models import FieldOption, FormField


def get_graphable_fields(form):
    return FormField.objects.filter(group__form=form).exclude(
        pk__in=FieldOption.objects.values_list('field__pk', flat=True)
    )
