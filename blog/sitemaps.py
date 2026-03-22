"""Sitemaps for SEO."""
from django.contrib.sitemaps import Sitemap
from .models import Post, Category


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.all()
