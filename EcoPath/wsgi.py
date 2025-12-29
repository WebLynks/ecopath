import os

from django.core.wsgi import get_wsgi_application

# NOTE: Ensure DJANGO_SETTINGS_MODULE is set in your production environment
# to point to 'settings.production'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings.dev')

application = get_wsgi_application()
