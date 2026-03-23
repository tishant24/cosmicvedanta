"""Blog URL routes."""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment_view, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment_view, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path('submit/', views.submit_post_view, name='submit_post'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('go/<slug:short_code>/', views.affiliate_redirect_view, name='affiliate_redirect'),
]
