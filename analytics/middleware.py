"""Middleware to track post views and produce Kafka events."""
from django.conf import settings
from django.utils import timezone

from .kafka_producer import produce_event


class PostViewTrackingMiddleware:
    """Track post detail views and produce analytics events."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only track successful post detail views
        if (
            request.resolver_match
            and request.resolver_match.url_name == 'post_detail'
            and response.status_code == 200
        ):
            slug = request.resolver_match.kwargs.get('slug', '')
            produce_event(
                topic=settings.KAFKA_TOPICS['POST_VIEWS'],
                event_data={
                    'event': 'post_view',
                    'post_slug': slug,
                    'user_id': request.user.pk if request.user.is_authenticated else None,
                    'session_key': request.session.session_key or '',
                    'ip_hash': str(hash(request.META.get('REMOTE_ADDR', '')))[:12],
                    'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
                    'referrer': request.META.get('HTTP_REFERER', '')[:500],
                    'timestamp': timezone.now().isoformat(),
                },
                key=slug,
            )

        return response
