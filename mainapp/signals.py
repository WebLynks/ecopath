from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project, Blog
from .utils import slugify_unique

@receiver(pre_save, sender=Project)
def create_project_slug(sender, instance, **kwargs):
    """Auto-generates a unique slug for a Project instance before saving."""
    if not instance.slug:
        instance.slug = slugify_unique(instance, value_field='title')

@receiver(pre_save, sender=Blog)
def create_blog_slug(sender, instance, **kwargs):
    """Auto-generates a unique slug for a Blog instance before saving."""
    if not instance.slug:
        instance.slug = slugify_unique(instance, value_field='title')

# NOTE: You can add more signals here, for example:
# - A pre_save signal to validate uploaded image sizes using the image_validate_and_resize utility.
# - A post_save signal for ContactSubmission to enqueue a background task for sending emails,
#   making the contact form submission faster for the user.
