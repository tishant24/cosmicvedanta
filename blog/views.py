"""Blog views: home feed, post detail, category, comments, user posts."""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseForbidden
from django.utils.text import slugify

from .models import Post, Category, Comment, AffiliateLink, UserPost
from .forms import CommentForm, CommentEditForm, UserPostForm, AdminPostForm


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


@login_required
def edit_comment_view(request, comment_id):
    """Edit own comment."""
    comment = get_object_or_404(Comment, pk=comment_id)

    # Only the comment author can edit
    if comment.author != request.user:
        return HttpResponseForbidden("You can only edit your own comments.")

    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.is_edited = True
            comment.save()
            messages.success(request, 'Comment updated.')
            return redirect('blog:post_detail', slug=comment.post.slug)
    else:
        form = CommentEditForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'comment': comment,
    })


@login_required
def delete_comment_view(request, comment_id):
    """Delete own comment."""
    comment = get_object_or_404(Comment, pk=comment_id)

    # Only the comment author can delete
    if comment.author != request.user:
        return HttpResponseForbidden("You can only delete your own comments.")

    post_slug = comment.post.slug
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted.')
        return redirect('blog:post_detail', slug=post_slug)

    return render(request, 'blog/delete_comment.html', {
        'comment': comment,
    })


@login_required
def submit_post_view(request):
    """Allow any user to submit a post. Admin posts auto-publish."""
    is_admin = request.user.is_staff or request.user.is_superuser

    if is_admin:
        # Admin gets the full post form — publishes directly
        if request.method == 'POST':
            form = AdminPostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                if not post.slug:
                    post.slug = slugify(post.title)
                post.status = 'published'
                if not post.excerpt:
                    post.excerpt = post.body[:200]
                post.save()
                messages.success(request, 'Post published successfully!')
                return redirect('blog:post_detail', slug=post.slug)
        else:
            form = AdminPostForm()
        return render(request, 'blog/admin_post.html', {'form': form})
    else:
        # Regular users submit for approval
        if request.method == 'POST':
            form = UserPostForm(request.POST, request.FILES)
            if form.is_valid():
                user_post = form.save(commit=False)
                user_post.author = request.user
                user_post.save()
                messages.success(request, 'Your post has been submitted for review!')
                return redirect('blog:my_posts')
        else:
            form = UserPostForm()
        return render(request, 'blog/submit_post.html', {'form': form})


@login_required
def my_posts_view(request):
    """Show user their submitted posts and their status."""
    user_posts = UserPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {
        'user_posts': user_posts,
    })


@login_required
def admin_dashboard_view(request):
    """Admin dashboard to approve/reject user posts from frontend."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Admin access only.")

    pending = UserPost.objects.filter(status='pending')
    approved = UserPost.objects.filter(status='approved')[:10]
    rejected = UserPost.objects.filter(status='rejected')[:10]

    return render(request, 'blog/admin_dashboard.html', {
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    })


@login_required
def approve_post_view(request, post_id):
    """Approve a user post from frontend — creates a published Post."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Admin access only.")

    user_post = get_object_or_404(UserPost, pk=post_id)

    if request.method == 'POST':
        user_post.status = 'approved'
        user_post.save()

        # Create actual published Post
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

        messages.success(request, f'"{user_post.title}" approved and published!')
        return redirect('blog:admin_dashboard')

    return render(request, 'blog/approve_post.html', {'user_post': user_post})


@login_required
def reject_post_view(request, post_id):
    """Reject a user post with reason."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Admin access only.")

    user_post = get_object_or_404(UserPost, pk=post_id)

    if request.method == 'POST':
        user_post.status = 'rejected'
        user_post.admin_note = request.POST.get('reason', '')
        user_post.save()
        messages.success(request, f'"{user_post.title}" rejected.')
        return redirect('blog:admin_dashboard')

    return render(request, 'blog/reject_post.html', {'user_post': user_post})


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
