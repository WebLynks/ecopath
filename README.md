# EcoPath - Monolithic Django Project

EcoPath is a production-ready, monolithic Django project designed for a corporate or portfolio website. It features a single app (`mainapp`) that serves all HTML pages and static assets, with a focus on security, robustness, and maintainability.

## Features

- **Single App Architecture**: All logic is contained within `mainapp` for simplicity.
- **Production-Ready Settings**: Separate settings for development and production, with security headers and environment-based configuration using `python-decouple`.
- **Curated Admin Interface**: Built with `django-jazzmin` and `django-admin-charts` for a modern, user-friendly admin experience.
- **Rich Content Editing**: `django-ckeditor` is integrated for easy creation of rich text content.
- **Internal Analytics**: A custom `HitCount` model tracks page views with debouncing to provide insights into content popularity.
- **Secure Contact Form**: Includes rate-limiting and a honeypot field to prevent spam.
- **Utility Commands**: Management commands for cleaning up orphaned media files and recomputing analytics.

## Quickstart (Development)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd EcoPath
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Copy the example environment file and fill in the required values.
    ```bash
    cp .env.example .env
    ```
    You will need to set a `SECRET_KEY`. The default database is SQLite, which requires no further configuration.

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## Running Tests

To run the test suite, use `pytest`:

```bash
pytest
```

## Management Commands

-   **Recompute Hit Counts**: Aggregate and display total hits for projects and blogs.
    ```bash
    python manage.py recompute_hit_counts
    ```

-   **Cleanup Orphan Uploads**: Find and remove media files that are no longer referenced in the database.
    ```bash
    python manage.py cleanup_orphan_uploads --dry-run  # To list files without deleting
    python manage.py cleanup_orphan_uploads           # To delete files (with confirmation)
    ```

## Deployment Checklist

1.  **Environment Variables**: Create a `.env.prod` file on the server with production-level settings (e.g., `DEBUG=False`, a strong `SECRET_KEY`, database credentials, `ALLOWED_HOSTS`).
2.  **Set `DJANGO_SETTINGS_MODULE`**: Ensure the environment variable `DJANGO_SETTINGS_MODULE` is set to `settings.production` in your production environment (e.g., in your Gunicorn service file).
3.  **Collect Static Files**: Run `python manage.py collectstatic` to gather all static files into `STATIC_ROOT`.
4.  **Web Server (Nginx)**: Configure Nginx to serve static and media files directly and proxy dynamic requests to Gunicorn. An example configuration is provided in `nginx/nginx_site.conf`.
5.  **Application Server (Gunicorn)**: Use the provided `gunicorn.service` template to run Gunicorn as a systemd service.
6.  **HTTPS**: Secure your site with an SSL certificate (e.g., using Let's Encrypt).
7.  **Security**: Review and enable all security settings in `settings/production.py`, such as `SECURE_HSTS_SECONDS`.
