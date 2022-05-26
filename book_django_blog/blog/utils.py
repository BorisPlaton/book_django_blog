from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.base import ContextMixin
from taggit.models import Tag

from blog.models import Post


class TagMixin(ContextMixin, View):
    tag = None

    def get_posts_with_tag(self):
        posts = Post.objects.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[self.tag])
            print(posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


def share_post_via_email(data: dict):
    subject = f"{data['name']} ({data['email']}) recommends you reading \"{data['post_title']}\""
    message = f"Read \"{data['post_title']}\" at {data['post_url']}\n\n" \
              f"{data['name']}\'s comments: {data['comments']}"
    status = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [data['to']],
    )

    return bool(status)


def get_similar_posts(post: Post):
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = (Post.objects
                     .filter(tags__in=post_tags_ids)
                     .exclude(pk=post.pk)
                     .annotate(same_tags=Count(Q(tags__in=post_tags_ids)))
                     .order_by('-same_tags')
                     )
    return similar_posts
