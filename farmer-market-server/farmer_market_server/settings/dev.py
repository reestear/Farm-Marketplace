import os

import dj_database_url

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if os.getenv("DEV_USE_DB") == "TRUE":
    DATABASES = {"default": dj_database_url.config(default=os.getenv("POSTGRES_URL"))}
else:
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

print("DEV SETTINGS LOADED", flush=True)
