from .base import *

# Production-specific settings
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ecopath.earth', cast=Csv())

# Security settings for production
# NOTE: Ensure your site is served over HTTPS before enabling these settings permanently.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files storage
# Use WhiteNoise to serve static files directly from Gunicorn in production.
# http://whitenoise.evans.io/en/stable/django.html
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging
# NOTE: Configure Sentry or another logging service for production error tracking.
SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# Caching (use Redis in production)
# NOTE: Ensure the CACHE_URL environment variable is set to your Redis instance.
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('CACHE_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
