from django import template
from django.db.models import Count
import markdown as md
from django.utils.safestring import mark_safe

from blog.forms import SearchForm
from blog.models import Post


register = template.Library()


@register.simple_tag
def form_control(field, **kwargs):
    additional_class_arg = kwargs.pop('class', '')
    field.field.widget.attrs.update(
        {
            'class': 'form-control form-control-sm ' + additional_class_arg,
        }
    )
    if kwargs:
        field.field.widget.attrs.update({key: value for key, value in kwargs.items()})
    return field


@register.inclusion_tag('blog/includes/search_form.html')
def search_form():
    return {'form': SearchForm}


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(md.markdown(text, extensions=['tables']))
