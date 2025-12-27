from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
import logging

from django.utils.decorators import method_decorator

from .models import Project, ProjectHomeBanner, Blog, Clientele, Testimonial, HomepageTestimonial, TeamMember, HitCount, ContactSubmission
from .forms import ContactForm
from .utils import format_contact_email

logger = logging.getLogger(__name__)

class HomepageView(TemplateView):
    template_name = "mainapp/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # NOTE: For performance on large datasets, consider caching these querysets.
        # Avoid order_by('?') on large tables; fetch random IDs in a more performant way if needed.
        context['featured_projects'] = Project.objects.filter(status='PUBLISHED', is_featured_home=True).order_by('-created_at')[:3]
        context['recent_blogs'] = Blog.objects.filter(status='PUBLISHED').order_by('-published_date')[:3]
        context['clients'] = Clientele.objects.all()
        context['featured_testimonials'] = Testimonial.objects.filter(is_featured=True)
        context['home_project_banners'] = ProjectHomeBanner.objects.all()
        context['homepage_testimonials'] = HomepageTestimonial.objects.all()
        print(len(HomepageTestimonial.objects.all()))
        return context

class ProjectListView(ListView):
    model = Project
    template_name = "mainapp/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.filter(status='PUBLISHED').only('title', 'slug', 'header_image_desktop', 'brief_description').order_by('-created_at')

class ProjectDetailView(DetailView):
    model = Project
    template_name = "mainapp/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(status='PUBLISHED')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Safely increment hit count
        HitCount.objects.increment(self.object, request=self.request)
        return response

class BlogListView(ListView):
    model = Blog
    template_name = "mainapp/blog_list.html"
    context_object_name = "blogs"

    def get_queryset(self):
        return Blog.objects.filter(status='PUBLISHED').order_by('-published_date')

class BlogDetailView(DetailView):
    model = Blog
    template_name = "mainapp/blog_detail.html"
    context_object_name = "blog"

    def get_queryset(self):
        return Blog.objects.filter(status='PUBLISHED')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        HitCount.objects.increment(self.object, request=self.request)
        return response

class ContactView(CreateView):
    model = ContactSubmission
    form_class = ContactForm
    template_name = "mainapp/contact.html"
    def get_success_url(self):
        return reverse_lazy('mainapp:contact') + '?success=1'

    def form_valid(self, form):
        # Honeypot check
        # If form has a honeypot field check it defensively
        if form.cleaned_data.get('honeypot'):
            return HttpResponseRedirect(self.get_success_url())

        self.object = form.save(commit=False)

        try:
            with transaction.atomic():
                self.object.save()
                subject, text_body, html_body = format_contact_email(self.object)

                # NOTE: For production, this email sending should be offloaded to a background worker
                send_mail(
                    subject=subject,
                    message=text_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                    html_message=html_body,
                    fail_silently=False
                )

        except Exception as e:
            logger.error(f"Failed to send contact submission email for {getattr(self.object, 'email', 'unknown')}: {e}")
            # Continue to success page even if email fails

        return HttpResponseRedirect(self.get_success_url())

class AboutUsView(TemplateView):
    template_name = "mainapp/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        context['recent_blogs'] = Blog.objects.filter(status='PUBLISHED').order_by('-published_date')[:3]
        return context

# Placeholder Views
class TechnologyProductsView(TemplateView):
    template_name = "mainapp/technology_products.html"

class ServicesView(TemplateView):
    template_name = "mainapp/services.html"

class SustainabilityView(TemplateView):
    template_name = "mainapp/sustainability.html"
