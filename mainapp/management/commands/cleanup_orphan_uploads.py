import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.db import models

class Command(BaseCommand):
    help = 'Scans the media directory and removes files not referenced by any model.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Don't delete files, just list the ones that would be deleted.",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting orphan file cleanup...'))
        dry_run = options['dry_run']

        # 1. Get all file paths from models
        referenced_files = set()
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if isinstance(field, models.FileField):
                    # Get all non-empty file paths for this field
                    storage = field.storage
                    for value in model.objects.values_list(field.name, flat=True):
                        if value:
                            referenced_files.add(storage.path(value))

        self.stdout.write(f'Found {len(referenced_files)} referenced files in the database.')

        # 2. Walk through the media directory
        media_root = settings.MEDIA_ROOT
        orphaned_files = []
        for root, _, files in os.walk(media_root):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filepath not in referenced_files:
                    orphaned_files.append(filepath)

        # 3. Report and optionally delete orphans
        if not orphaned_files:
            self.stdout.write(self.style.SUCCESS('No orphaned files found.'))
            return

        self.stdout.write(self.style.WARNING(f'Found {len(orphaned_files)} orphaned files:'))
        for f in orphaned_files:
            self.stdout.write(f' - {f}')

        if not dry_run:
            if input('Are you sure you want to delete these files? (y/N) ').lower() == 'y':
                for f in orphaned_files:
                    os.remove(f)
                self.stdout.write(self.style.SUCCESS('Deleted orphaned files.'))
            else:
                self.stdout.write(self.style.NOTICE('Operation cancelled.'))
        else:
            self.stdout.write(self.style.NOTICE('Dry run complete. No files were deleted.'))
