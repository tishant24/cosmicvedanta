import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cosmicvedanta.settings'
django.setup()

from django.utils import timezone
from blog.models import Post

posts = Post.objects.all()
print(f"Total posts: {posts.count()}")

for p in posts:
    print(f"  - '{p.title}' | status={p.status} | published_at={p.published_at} | featured={p.is_featured}")
    if p.status == 'published' and not p.published_at:
        p.published_at = timezone.now()
        p.save()
        print(f"    -> Fixed: set published_at")

# Force re-save all published posts to ensure published_at is set
for p in Post.objects.filter(status='published'):
    if not p.published_at:
        p.published_at = timezone.now()
    p.save()
    print(f"  Re-saved: {p.title}")

print("\nDone! All posts should now appear.")
