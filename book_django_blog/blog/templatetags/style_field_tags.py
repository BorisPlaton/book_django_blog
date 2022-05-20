from django import template

register = template.Library()


@register.simple_tag
def form_control(field):
    field.field.widget.attrs.update(
        {
            'class': 'form-control form-control-sm'
        }
    )
    return field
