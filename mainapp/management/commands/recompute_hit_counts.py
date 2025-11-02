from django.core.management.base import BaseCommand
from django.db.models import Sum
from mainapp.models import HitCount, Project, Blog

class Command(BaseCommand):
    help = 'Recomputes and caches aggregated hit counts for content objects.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting hit count recomputation...'))

        # Example for Projects
        projects = Project.objects.filter(status='PUBLISHED')
        for project in projects:
            total_hits = HitCount.objects.filter(object_id=project.pk, content_type__model='project').aggregate(total=Sum('hits'))['total'] or 0
            # Here you would typically update a cached value or a denormalized field on the Project model.
            # For this example, we'll just print the result.
            self.stdout.write(f'Project "{project.title}" has {total_hits} total hits.')

        # Example for Blogs
        blogs = Blog.objects.filter(status='PUBLISHED')
        for blog in blogs:
            total_hits = HitCount.objects.filter(object_id=blog.pk, content_type__model='blog').aggregate(total=Sum('hits'))['total'] or 0
            self.stdout.write(f'Blog "{blog.title}" has {total_hits} total hits.')

        self.stdout.write(self.style.SUCCESS('Finished hit count recomputation.'))
