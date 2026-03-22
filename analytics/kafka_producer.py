"""
Kafka event producer for streaming analytics events.

Events are produced to Kafka topics for downstream processing via:
Azure Data Lake Storage (ADLS) -> Unity Catalog -> Delta Lake

When KAFKA_ENABLED is False, events are logged to console for development.
"""
import json
import logging
from django.conf import settings

logger = logging.getLogger('cosmicvedanta.analytics')

_producer = None


def _get_producer():
    """Lazy-initialize Kafka producer."""
    global _producer
    if _producer is None and settings.KAFKA_ENABLED:
        try:
            from kafka import KafkaProducer
            _producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1,
            )
            logger.info('Kafka producer initialized: %s', settings.KAFKA_BOOTSTRAP_SERVERS)
        except Exception as e:
            logger.error('Failed to initialize Kafka producer: %s', e)
            _producer = None
    return _producer


def produce_event(topic, event_data, key=None):
    """
    Produce an event to a Kafka topic.

    Args:
        topic: Kafka topic name.
        event_data: dict of event payload.
        key: optional partition key.
    """
    if not settings.KAFKA_ENABLED:
        logger.info('[KAFKA-DEV] Topic=%s | Key=%s | Data=%s', topic, key, json.dumps(event_data))
        return

    producer = _get_producer()
    if producer is None:
        logger.warning('Kafka producer unavailable. Event dropped: %s', event_data)
        return

    try:
        future = producer.send(topic, value=event_data, key=key)
        future.add_callback(
            lambda meta: logger.debug(
                'Event sent to %s [partition=%s, offset=%s]',
                meta.topic, meta.partition, meta.offset,
            )
        )
        future.add_errback(
            lambda exc: logger.error('Failed to send event to %s: %s', topic, exc)
        )
    except Exception as e:
        logger.error('Kafka produce error for topic %s: %s', topic, e)
