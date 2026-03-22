"""Global template context processors for SEO defaults."""
from django.conf import settings


def seo_defaults(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_description': settings.SITE_DESCRIPTION,
        'site_url': settings.SITE_URL,
    }
