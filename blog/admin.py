"""Admin configuration for blog models."""
from django.contrib import admin
from django.utils.text import slugify
from .models import Category, Post, Comment, AffiliateLink, UserPost


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'view_count', 'published_at')
    list_filter = ('status', 'category', 'is_featured', 'is_premium')
    search_fields = ('title', 'body', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    raw_id_fields = ('author',)

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'category', 'status')}),
        ('Content', {'fields': ('featured_image', 'excerpt', 'body', 'body_raw')}),
        ('Philosophy', {'fields': ('vedanta_quote', 'vedanta_source'), 'classes': ('collapse',)}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords'), 'classes': ('collapse',)}),
        ('Settings', {'fields': ('is_featured', 'is_premium', 'published_at')}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_approved', 'is_edited', 'created_at', 'parent')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('body', 'author__email', 'author__display_name')
    actions = ['approve_comments', 'reject_comments']

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Reject selected comments')
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'body', 'author__email', 'author__display_name')
    readonly_fields = ('author', 'title', 'body', 'image', 'category', 'created_at')
    actions = ['approve_posts', 'reject_posts']

    fieldsets = (
        ('Submission', {'fields': ('author', 'title', 'category', 'body', 'image', 'created_at')}),
        ('Review', {'fields': ('status', 'admin_note')}),
    )

    def save_model(self, request, obj, form, change):
        """When admin saves with status=approved, auto-create a published Post."""
        super().save_model(request, obj, form, change)
        if obj.status == 'approved':
            # Check if Post already exists for this UserPost
            slug = slugify(obj.title)
            if not Post.objects.filter(slug=slug).exists():
                post = Post(
                    title=obj.title,
                    slug=slug,
                    author=obj.author,
                    category=obj.category,
                    body=obj.body,
                    excerpt=obj.body[:200],
                    status='published',
                )
                if obj.image:
                    post.featured_image = obj.image
                post.save()

    @admin.action(description='Approve selected posts')
    def approve_posts(self, request, queryset):
        for user_post in queryset.filter(status='pending'):
            slug = slugify(user_post.title)
            if not Post.objects.filter(slug=slug).exists():
                post = Post(
                    title=user_post.title,
                    slug=slug,
                    author=user_post.author,
                    category=user_post.category,
                    body=user_post.body,
                    excerpt=user_post.body[:200],
                    status='published',
                )
                if user_post.image:
                    post.featured_image = user_post.image
                post.save()
            user_post.status = 'approved'
            user_post.save()

    @admin.action(description='Reject selected posts')
    def reject_posts(self, request, queryset):
        queryset.update(status='rejected')


@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'is_active', 'click_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'short_code')
