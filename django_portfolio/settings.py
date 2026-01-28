from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "1") == "1"

# Hosts desde .env (opcional) + defaults
env_hosts = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]

ALLOWED_HOSTS = list(dict.fromkeys(
    env_hosts + [
        "localhost",
        "127.0.0.1",
        ".onrender.com",
    ]
))

# Si tienes dominio propio en Render, ponlo aquí o en ALLOWED_HOSTS del .env
# ALLOWED_HOSTS += ["hoja-de-vida-neyser.onrender.com", "hoja-de-vida-neyser.render.com"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "https://*.onrender.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary (opcional)
    "cloudinary",
    "cloudinary_storage",

    "cv",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_portfolio.urls"
WSGI_APPLICATION = "django_portfolio.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # si no usas carpeta templates global, no pasa nada
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================
# DATABASE
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================
# STATIC
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =========================
# MEDIA (Cloudinary si hay credenciales; si no, local)
# =========================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUD_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUD_SECRET = os.getenv("CLOUDINARY_API_SECRET")

USE_CLOUDINARY = bool(CLOUD_NAME and CLOUD_KEY and CLOUD_SECRET)

if USE_CLOUDINARY:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUD_NAME,
        "API_KEY": CLOUD_KEY,
        "API_SECRET": CLOUD_SECRET,
    }
else:
    # local
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"