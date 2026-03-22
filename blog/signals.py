"""Signals for blog events -> Kafka."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Comment
from analytics.kafka_producer import produce_event


@receiver(post_save, sender=Comment)
def comment_created_event(sender, instance, created, **kwargs):
    """Produce a Kafka event when a new comment is posted."""
    if created:
        produce_event(
            topic=settings.KAFKA_TOPICS['COMMENTS'],
            event_data={
                'event': 'new_comment',
                'comment_id': instance.pk,
                'post_id': instance.post_id,
                'post_slug': instance.post.slug,
                'author_id': instance.author_id,
                'is_reply': instance.is_reply,
                'parent_id': instance.parent_id,
                'timestamp': instance.created_at.isoformat(),
            },
        )
