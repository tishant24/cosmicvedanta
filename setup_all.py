"""One script to set up everything on PythonAnywhere."""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cosmicvedanta.settings'
django.setup()

from django.utils import timezone
from blog.models import Post, Category
from accounts.models import CustomUser

# 1. Ensure categories exist
print("=== Creating Categories ===")
for name in ['Cosmos', 'Vedanta', 'Simulation Theory']:
    cat, created = Category.objects.get_or_create(name=name, defaults={'slug': name.lower().replace(' ', '-')})
    print(f"  {'Created' if created else 'Exists'}: {name}")

# 2. Get/fix author
author = CustomUser.objects.first()
if author:
    author.display_name = 'Tishant'
    author.save()
    print(f"\n=== Author: {author.email} (display: {author.display_name}) ===")
else:
    print("ERROR: No user found! Run: python manage.py createsuperuser")
    sys.exit(1)

cat_vedanta = Category.objects.get(name='Vedanta')

# 3. Create Post 1 - Architecture of Nothingness
print("\n=== Creating Post 1: Architecture of Nothingness ===")
p1, created = Post.objects.get_or_create(
    slug='architecture-of-nothingness-how-circle-birthed-digital-universe',
    defaults={
        'title': 'The Architecture of Nothingness: How a Simple Circle Birthed the Digital Universe',
        'author': author,
        'category': cat_vedanta,
        'status': 'published',
        'is_featured': True,
        'published_at': timezone.now(),
        'excerpt': 'From the meditative minds of ancient philosophers to deep-space servers of the modern web, the story of zero is the story of us.',
        'vedanta_quote': 'Shunya — the ultimate void, the blank canvas upon which the illusion of reality (Maya) is painted.',
        'vedanta_source': 'Vedantic Philosophy of Shunya',
        'body': '<p>Imagine a time when humanity had no word for the void...</p><p>The story of zero is the story of us.</p>',
    }
)
if not created:
    if not p1.published_at:
        p1.published_at = timezone.now()
    p1.status = 'published'
    p1.is_featured = True
    p1.save()
print(f"  {'Created' if created else 'Updated'} | status={p1.status} | published_at={p1.published_at}")

# 4. Create Post 2 - Mandukya Upanishad
print("\n=== Creating Post 2: Mandukya Upanishad ===")
p2, created = Post.objects.get_or_create(
    slug='mandukya-upanishad-essence-four-states-consciousness-om',
    defaults={
        'title': 'Mandukya Upanishad: The 12 Verses That Map the Entire Architecture of Consciousness',
        'author': author,
        'category': cat_vedanta,
        'status': 'published',
        'is_featured': True,
        'published_at': timezone.now(),
        'excerpt': 'In just 12 verses, the Mandukya Upanishad reveals that you are not a person experiencing the universe — you are the awareness in which the universe appears.',
        'vedanta_quote': 'This Self is Brahman. You are not a person experiencing the universe. You are the awareness in which the universe appears.',
        'vedanta_source': 'Mandukya Upanishad',
        'body': '<p>The Mandukya Upanishad — the shortest of all principal Upanishads, yet the most profound.</p>',
    }
)
if not created:
    if not p2.published_at:
        p2.published_at = timezone.now()
    p2.status = 'published'
    p2.is_featured = True
    p2.save()
print(f"  {'Created' if created else 'Updated'} | status={p2.status} | published_at={p2.published_at}")

# 5. Final check
print("\n=== All Posts ===")
for p in Post.objects.all():
    print(f"  [{p.status}] {p.title}")
    print(f"    slug: {p.slug}")
    print(f"    published_at: {p.published_at}")
    print(f"    featured: {p.is_featured}")
    print(f"    author: {p.author}")
    print()

print("DONE! Reload your web app now.")
