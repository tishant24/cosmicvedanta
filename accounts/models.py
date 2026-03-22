"""Custom User model supporting Email and Mobile Number authentication."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Manager for CustomUser with email/mobile support."""

    def create_user(self, email=None, mobile=None, password=None, **extra_fields):
        if not email and not mobile:
            raise ValueError('Users must provide either an email or mobile number.')
        if email:
            email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, mobile=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not email:
            raise ValueError('Superusers must have an email address.')
        return self.create_user(email=email, mobile=mobile, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model allowing login via email or mobile number."""

    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    # OTP fields for mobile verification
    otp_code = models.CharField(max_length=6, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Newsletter / freemium
    subscribed_newsletter = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.display_name or self.email or self.mobile or f'User #{self.pk}'

    def get_short_name(self):
        return self.display_name or self.email or self.mobile

    def generate_otp(self):
        """Generate a 6-digit OTP for mobile verification."""
        import random
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save(update_fields=['otp_code', 'otp_created_at'])
        return self.otp_code

    def verify_otp(self, code):
        """Verify OTP code. Valid for 10 minutes."""
        from datetime import timedelta
        if (
            self.otp_code == code
            and self.otp_created_at
            and timezone.now() - self.otp_created_at < timedelta(minutes=10)
        ):
            self.is_mobile_verified = True
            self.otp_code = ''
            self.save(update_fields=['is_mobile_verified', 'otp_code'])
            return True
        return False
