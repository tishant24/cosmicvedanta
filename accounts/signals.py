"""Signals for user signup events -> Kafka."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import CustomUser
from analytics.kafka_producer import produce_event


@receiver(post_save, sender=CustomUser)
def user_signup_event(sender, instance, created, **kwargs):
    """Produce a Kafka event when a new user signs up."""
    if created:
        produce_event(
            topic=settings.KAFKA_TOPICS['USER_SIGNUPS'],
            event_data={
                'event': 'user_signup',
                'user_id': instance.pk,
                'email': instance.email or '',
                'mobile': instance.mobile or '',
                'display_name': instance.display_name,
                'signup_method': 'email' if instance.email else 'mobile',
                'timestamp': instance.date_joined.isoformat(),
            },
        )
