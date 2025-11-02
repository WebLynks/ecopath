import hashlib
from typing import Type
from django.db import models
from django.utils.text import slugify

def slugify_unique(instance: Type[models.Model], value_field: str = 'title', slug_field: str = 'slug') -> str:
    """
    Generates a unique slug for a model instance.
    """
    slug = slugify(getattr(instance, value_field))
    qs = instance.__class__.objects.filter(**{slug_field: slug})
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    
    if qs.exists():
        # Append a number to make the slug unique
        i = 1
        while True:
            new_slug = f"{slug}-{i}"
            if not instance.__class__.objects.filter(**{slug_field: new_slug}).exists():
                slug = new_slug
                break
            i += 1
    return slug

def get_visitor_key(request) -> str:
    """
    Returns a hashed key for the visitor based on session or IP and User-Agent.
    """
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    ip_address = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Use session key for logged-in users or a hash of IP+UA for anonymous users
    if request.user.is_authenticated:
        key_string = f"{request.user.pk}:{session_key}"
    else:
        key_string = f"{ip_address}:{user_agent}"
        
    return hashlib.sha256(key_string.encode('utf-8')).hexdigest()

# NOTE: The following functions are placeholders. A robust implementation would involve
# more detailed logic, especially for image processing.

def image_validate_and_resize(file, max_size_mb: int = 5, max_width: int = 2500):
    """
    Placeholder for image validation and resizing logic.
    - Validates file size, content type (MIME).
    - Resizes image if it exceeds max_width.
    """
    # from PIL import Image
    # from django.core.exceptions import ValidationError
    #
    # if file.size > max_size_mb * 1024 * 1024:
    #     raise ValidationError(f"Image size cannot exceed {max_size_mb}MB.")
    #
    # # ... more validation and resizing logic using Pillow ...
    pass

def format_contact_email(submission) -> tuple[str, str]:
    """
    Formats the contact submission into plain text and HTML email bodies.
    """
    subject = f"New Contact Inquiry from {submission.first_name} {submission.last_name}"
    
    # Basic plain text body
    text_body = (
        f"You have received a new contact submission:\n\n"
        f"Name: {submission.first_name} {submission.last_name}\n"
        f"Email: {submission.email}\n"
        f"Mobile: {submission.mobile_number or 'N/A'}\n"
        f"Service Inquiry: {submission.service_inquiry.name}\n"
        f"Message: {submission.message}\n\n"
        f"-- Technical Details --\n"
        f"IP Address: {submission.ip_address}\n"
        f"Device Info: {submission.device_info}"
    )
    
    # Basic HTML body
    html_body = (
        f"<html><body>"
        f"<h2>New Contact Inquiry</h2>"
        f"<p><strong>Name:</strong> {submission.first_name} {submission.last_name}</p>"
        f"<p><strong>Email:</strong> {submission.email}</p>"
        f"<p><strong>Mobile:</strong> {submission.mobile_number or 'N/A'}</p>"
        f"<p><strong>Service Inquiry:</strong> {submission.service_inquiry.name}</p>"
        f"<p><strong>Message:</strong><br>{submission.message}</p>"
        f"<hr>"
        f"<h3>Technical Details</h3>"
        f"<p><strong>IP Address:</strong> {submission.ip_address}</p>"
        f"<p><strong>Device Info:</strong> {submission.device_info}</p>"
        f"</body></html>"
    )
    
    return subject, text_body, html_body
