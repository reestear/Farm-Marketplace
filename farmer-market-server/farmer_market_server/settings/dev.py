import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "database" / "db.sqlite3",
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DJANGO_POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "TEST": {"NAME": BASE_DIR / "test_farmer_market_db.sqlite3"},
    }
}

MEDIA_ROOT = BASE_DIR / "media"  # store locally
MEDIA_URL = "/api/media/"

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/api/static/"

# Email backend
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
