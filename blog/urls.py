"""Blog URL routes."""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment_view, name='add_comment'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('go/<slug:short_code>/', views.affiliate_redirect_view, name='affiliate_redirect'),
]
