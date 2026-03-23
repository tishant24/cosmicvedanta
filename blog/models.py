"""Blog models: Posts, Categories, Comments, and Affiliate Links."""
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from .formatter import format_plain_text


class Category(models.Model):
    """Post category (e.g., Cosmos, Vedanta, Simulation Theory)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(
        max_length=50, blank=True,
        help_text='CSS class for category icon (e.g., fa-star)',
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class Post(models.Model):
    """Daily article / blog post."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts',
    )
    featured_image = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    excerpt = models.TextField(max_length=500, blank=True, help_text='Short summary for SEO and cards.')
    body = models.TextField(help_text='Write plain text — it auto-formats to styled HTML. Or use HTML directly.')
    body_raw = models.TextField(blank=True, help_text='Original plain text (auto-saved).')

    # Philosophy integration
    vedanta_quote = models.TextField(
        blank=True,
        help_text='A Vedanta or philosophical quote to highlight alongside the post.',
    )
    vedanta_source = models.CharField(
        max_length=200, blank=True,
        help_text='Source of the quote (e.g., Upanishads, Bhagavad Gita).',
    )

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True, help_text='SEO title (max 70 chars).')
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO description (max 160 chars).')
    meta_keywords = models.CharField(max_length=255, blank=True)

    # Publishing
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False, help_text='Restrict to premium users.')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Analytics
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        # Auto-format plain text to styled HTML
        from .formatter import is_plain_text
        if is_plain_text(self.body):
            self.body_raw = self.body
            cat_slug = self.category.slug if self.category else None
            self.body = format_plain_text(self.body, cat_slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_seo_title(self):
        return self.meta_title or self.title

    def get_seo_description(self):
        return self.meta_description or self.excerpt or self.body[:157] + '...'

    @property
    def category_theme(self):
        """Return CSS theme class based on category."""
        if not self.category:
            return 'theme-cosmos'
        slug = self.category.slug
        theme_map = {
            'cosmos': 'theme-cosmos',
            'vedanta': 'theme-vedanta',
            'simulation-theory': 'theme-simulation',
            'machine-learning': 'theme-study',
            'study-notes': 'theme-study',
            'data-engineering': 'theme-study',
            'physics': 'theme-study',
        }
        return theme_map.get(slug, 'theme-cosmos')


class Comment(models.Model):
    """Nested comment system for post discussions."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments',
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
    )
    body = models.TextField(max_length=2000)
    is_approved = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} on "{self.post.title}"'

    @property
    def is_reply(self):
        return self.parent is not None

    def get_replies(self):
        return Comment.objects.filter(parent=self, is_approved=True)


class UserPost(models.Model):
    """Community-submitted posts that require admin approval."""

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_posts',
    )
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
    )
    body = models.TextField(help_text='Your post content.')
    image = models.ImageField(upload_to='user_posts/%Y/%m/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True, help_text='Reason for rejection (shown to user).')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} by {self.author}'


class AffiliateLink(models.Model):
    """Managed affiliate links that can be inserted into posts."""
    name = models.CharField(max_length=200, help_text='Internal name for this affiliate link.')
    url = models.URLField(help_text='Full affiliate URL.')
    short_code = models.SlugField(
        max_length=50, unique=True,
        help_text='Short code to reference in posts, e.g., {{aff:my-book}}.',
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='affiliates/', blank=True)
    is_active = models.BooleanField(default=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:affiliate_redirect', kwargs={'short_code': self.short_code})
