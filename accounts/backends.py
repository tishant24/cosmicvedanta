"""Custom authentication backend for email or mobile login."""
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrMobileBackend:
    """Authenticate with either email or mobile number."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        # Try email first, then mobile
        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(mobile=username)
            except User.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
