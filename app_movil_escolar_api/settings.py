import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY desde entorno
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-secret-key")
# SECRET_KEY = '-_&+lsebec(whhw!%n@ww&1j=4-^j_if9x8$q778+99oz&!ms2'

# Debug por variable de entorno
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Hosts permitidos
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    os.environ.get("RENDER_EXTERNAL_HOSTNAME", ""),
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "app_movil_escolar_api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS CONFIG
CORS_ALLOWED_ORIGINS = ["http://localhost:4200", os.environ.get("FRONTEND_URL", "")]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "app_movil_escolar_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app_movil_escolar_api.wsgi.application"

# ------------------------------
#        DATABASE POSTGRES
# ------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=600, ssl_require=True
    )
}

# ------------------------------
#         REST FRAMEWORK
# ------------------------------
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "app_movil_escolar_api.models.BearerTokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

# ------------------------------
# STATIC & MEDIA
# ------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------
# TIME / LANGUAGE
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
