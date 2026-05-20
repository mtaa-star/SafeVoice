"""
WSGI config for SafeVoice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SafeVoice.settings')

application = get_wsgi_application()

# Create a default admin user at startup if one does not already exist.
# This allows access to the dashboard using ADMIN_USERNAME/ADMIN_PASSWORD.
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin@123')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
        )
except Exception:
    # Ignore failures during management commands or startup before DB is ready
    pass
