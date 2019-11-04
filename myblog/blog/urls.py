from django.urls import path

from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [
      path(
          route='<int:post_id>/share/',
          view=views.post_share,
          name='post_share'
      ),
      path(
          route='',
          view=views.post_list,
          name='post_list'
      ),
      path(
          route='<int:year>/<int:month>/<int:day>/<slug:post>/',
          view=views.post_detail,
          name='post_detail'
      ),
      path(
          route='tag/<slug:tag_slug>/',
          view=views.post_list,
          name='post_list_by_tag'
      ),
      path(
          route='feed/',
          view=LatestPostsFeed(),
          name='post_feed'
      ),
      path(
          route='search/',
          view=views.post_search,
          name='post_search'
      ),
]
