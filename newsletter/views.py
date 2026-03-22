"""Newsletter subscription views."""
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from .models import Subscriber
from analytics.kafka_producer import produce_event


@require_POST
def subscribe_view(request):
    """Handle newsletter subscription via email or mobile."""
    email = request.POST.get('email', '').strip()
    mobile = request.POST.get('mobile', '').strip()
    name = request.POST.get('name', '').strip()

    if not email and not mobile:
        messages.error(request, 'Please provide an email or mobile number.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    defaults = {'name': name, 'is_active': True}
    created = False

    if email:
        _, created = Subscriber.objects.get_or_create(email=email, defaults=defaults)
    elif mobile:
        _, created = Subscriber.objects.get_or_create(mobile=mobile, defaults=defaults)

    if created:
        messages.success(request, 'Welcome aboard, cosmic traveler! You are now subscribed.')
        produce_event(
            topic=settings.KAFKA_TOPICS['NEWSLETTER'],
            event_data={
                'event': 'newsletter_subscribe',
                'email': email,
                'mobile': mobile,
                'name': name,
            },
        )
    else:
        messages.info(request, 'You are already subscribed!')

    return redirect(request.META.get('HTTP_REFERER', '/'))
