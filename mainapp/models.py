from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.db.models import F
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# NOTE: Add image validation logic (e.g., file size, dimensions) in clean() methods
# or using signals for more robust validation before saving.

class ServiceCategory(models.Model):
    """Represents a category of service offered."""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Service Categories"

class Clientele(models.Model):
    """Represents a client or partner."""
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='clientele_logos/')
    website_url = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    """Represents a testimonial from a client."""
    quote = models.TextField()
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=150)
    author_image = models.ImageField(upload_to='testimonial_authors/', blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.quote[:30]}..." - {self.author_name}'


class HomepageTestimonial(models.Model):
    customer_name = models.CharField("Customer Name", max_length=75)
    customer_designation = models.CharField("Customer Designation", max_length=75)
    customer_image = models.ImageField("Customer Image", upload_to='homepage_testimonials/', blank=True)
    testimonial = models.TextField("Testimonial", max_length=300)

    def __str__(self):
        return self.customer_name

class TeamMember(models.Model):
    """Represents a member of the team. Not a Django user."""
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='team_photos/')
    linkedin_url = models.URLField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True, help_text="Lower numbers appear first.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Project(models.Model):
    """Represents a single project."""
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Auto-generated if left blank.")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    header_image_desktop = models.ImageField(upload_to='project_headers/desktop/')
    header_image_mobile = models.ImageField(upload_to='project_headers/mobile/')
    brief_description = models.TextField()
    detail_content = RichTextUploadingField()
    is_featured_home = models.BooleanField(default=False, db_index=True)
    author_name = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hitcount = GenericRelation('HitCount', object_id_field='object_id', content_type_field='content_type')

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    """Represents a gallery image for a Project."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='project_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.alt_text or f"Image for {self.project.title}"

class ProjectFact(models.Model):
    """A key-value fact associated with a project."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='facts')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('project', 'key')

    def __str__(self):
        return f"{self.key}: {self.value}"


class ProjectHomeBanner(models.Model):
    name = models.CharField("Name", max_length=100)
    scope = models.CharField("Scope", max_length=300)
    tech_used = models.CharField("Tech Used", max_length=200)
    performance_impact = models.CharField("Performance Impact", max_length=200)
    background_image = models.ImageField("Background Image", upload_to="project_home_banners/")
    cement_eliminated = models.CharField("Cement Eliminated", max_length=50)
    water_saved = models.CharField("Water Saved", max_length=50)

    def __str__(self):
        return self.name

class Blog(models.Model):
    """Represents a blog post."""
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Auto-generated if left blank.")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    summary = models.TextField()
    content = RichTextUploadingField()
    header_image_desktop = models.ImageField(upload_to='blog_headers/desktop/')
    header_image_mobile = models.ImageField(upload_to='blog_headers/mobile/')
    # NOTE: For a more robust tagging system, consider using a library like django-taggit.
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags.")
    published_date = models.DateTimeField(default=timezone.now, db_index=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hitcount = GenericRelation('HitCount', object_id_field='object_id', content_type_field='content_type')

    def __str__(self):
        return self.title

class ContactSubmission(models.Model):
    """Represents a submission from the contact form."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    mobile_number = models.CharField(max_length=20)
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Submission from {self.first_name} {self.last_name} ({self.email})"

    class Meta:
        ordering = ['-submission_date']

# --- Analytics Models ---

class HitCountManager(models.Manager):
    def increment(self, obj, request=None, delta=1, debounce_seconds=60):
        """
        Increments the hit count for a given object, with debouncing to prevent 
        rapid-fire increments from a single visitor.
        """
        if not obj:
            return

        content_type = ContentType.objects.get_for_model(obj)
        visitor_key = 'anonymous' # Fallback key

        # Generate a visitor key from session or IP + User-Agent
        if request:
            from .utils import get_visitor_key
            visitor_key = get_visitor_key(request)

        # Use cache to debounce hits from the same visitor
        cache_key = f"hit::{content_type.id}::{obj.pk}::{visitor_key}"
        cache = caches['default']
        
        # NOTE: This relies on a configured cache backend (e.g., Redis in prod).
        # If cache is not available, it will fall back to incrementing on every hit.
        if cache.get(cache_key):
            return # Debounce period is active, do not increment

        cache.set(cache_key, 1, timeout=debounce_seconds)

        # Get or create a HitCount row for today and update it atomically
        today = timezone.now().date()
        hit_count, created = self.get_or_create(
            content_type=content_type,
            object_id=obj.pk,
            created_at__date=today,
            defaults={'hits': 0}
        )

        hit_count.hits = F('hits') + delta
        hit_count.last_hit = timezone.now()
        hit_count.save(update_fields=['hits', 'last_hit'])

class HitCount(models.Model):
    """
    Tracks hits for any content object on a per-day basis.
    Allows for charting trends over time.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    hits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_hit = models.DateTimeField(auto_now=True)

    objects = HitCountManager()

    def __str__(self):
        return f"{self.content_object} - {self.hits} hits on {self.created_at.date()}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('content_type', 'object_id', 'created_at')
        verbose_name = 'Daily Hit Count'
        verbose_name_plural = 'Daily Hit Counts'
