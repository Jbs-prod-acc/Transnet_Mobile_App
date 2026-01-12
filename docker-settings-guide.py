"""
Docker-ready settings configuration.
This file provides environment variable support for Docker deployments.

Add this import at the top of your settings.py:
    import os
    
Replace hardcoded values with:

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DATABASE_NAME', 'mobility_transnet'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'malvapudding78*'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-6h=yduq(q!(b&n+tz0h4cdtg^@7)y_c!$+7pmw$**=-t@0@^t2')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
"""
