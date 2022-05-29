from django.urls import path

from blog import views
from blog.feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_with_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('share/<int:post_id>/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
