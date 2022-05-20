from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post
from .utils import share_post_via_email


class PostListView(ListView):
    queryset = Post.objects.get_published()
    context_object_name = 'posts'
    paginate_by = 15
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
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
