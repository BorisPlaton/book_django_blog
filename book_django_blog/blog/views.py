from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post
from .utils import share_post_via_email, get_similar_posts, TagMixin, get_search_results


class PostListView(TagMixin, ListView):
    context_object_name = 'posts'
    paginate_by = 15
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        return self.get_posts_with_tag()


def post_search(request):
    form = SearchForm(request.GET if 'query' in request.GET else None)
    search_results = query = None
    if form.is_valid():
        search_results, query = get_search_results(form.cleaned_data['query'])
    return render(request, 'blog/post/search.html', {'results': search_results})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    similar_posts = get_similar_posts(post)
    comments = post.comments.filter(active=True)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        form.save_comment(post=post)
        return redirect(post.get_absolute_url())

    return render(
        request, 'blog/post/detail.html',
        {
            'post': post,
            'form': form,
            'comments': comments,
            'similar_posts': similar_posts,
        }
    )


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        status='published'
    )
    form = EmailPostForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        data.update({
            'post_url': request.build_absolute_uri(post.get_absolute_url()),
            'post_title': post.title,
        })
        if share_post_via_email(data):
            messages.success(request, "Message was successfully sent")
            return redirect(post.get_absolute_url())

    return render(
        request, 'blog/post/share.html',
        {
            'post': post,
            'form': form,
        }
    )
