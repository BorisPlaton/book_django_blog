from django import template

register = template.Library()


@register.simple_tag
def form_control(field, **kwargs):
    field.field.widget.attrs.update(
        {
            'class': 'form-control form-control-sm',
        }
    )
    if kwargs:
        field.field.widget.attrs.update({key: value for key, value in kwargs.items()})
    return field
