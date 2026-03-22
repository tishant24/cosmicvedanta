"""Blog views: home feed, post detail, category, affiliate redirect."""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F

from .models import Post, Category, Comment, AffiliateLink
from .forms import CommentForm


def home_view(request):
    """Daily Universe Feed - main landing page."""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    featured = posts.filter(is_featured=True)[:3]

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)

    categories = Category.objects.all()

    return render(request, 'blog/home.html', {
        'posts': posts_page,
        'featured_posts': featured,
        'categories': categories,
    })


def post_detail_view(request, slug):
    """Single post with nested comments."""
    post = get_object_or_404(Post, slug=slug, status='published')

    # Increment view count
    Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)

    # Fetch top-level comments (not replies)
    comments = post.comments.filter(
        parent__isnull=True, is_approved=True
    ).select_related('author').prefetch_related('replies__author')

    comment_form = CommentForm()

    # Related posts
    related = Post.objects.filter(
        category=post.category, status='published'
    ).exclude(pk=post.pk)[:4]

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related,
    })


@login_required
def add_comment_view(request, slug):
    """Add a comment or reply to a post."""
    post = get_object_or_404(Post, slug=slug, status='published')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id = form.cleaned_data.get('parent_id')
            if parent_id:
                parent = Comment.objects.filter(pk=parent_id, post=post).first()
                comment.parent = parent

            comment.save()
            messages.success(request, 'Your comment has been posted!')
    return redirect('blog:post_detail', slug=slug)


def category_view(request, slug):
    """Posts filtered by category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)

    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts_page,
    })


def affiliate_redirect_view(request, short_code):
    """Track affiliate click and redirect."""
    link = get_object_or_404(AffiliateLink, short_code=short_code, is_active=True)
    AffiliateLink.objects.filter(pk=link.pk).update(click_count=F('click_count') + 1)
    return redirect(link.url)
