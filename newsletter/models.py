"""Newsletter subscription model."""
from django.db import models


class Subscriber(models.Model):
    """Newsletter subscriber (email or mobile)."""
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email or self.mobile or f'Subscriber #{self.pk}'
