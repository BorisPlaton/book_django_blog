from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = ''
    description = 'New posts of my blog'

    def items(self):
        return Post.objects.get_published()[:5]

    def items_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
