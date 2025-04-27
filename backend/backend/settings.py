import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from split_settings.tools import include


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'False') == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", '').split(', ')

COMPONENTS_DIR_NAME = 'components'

# Application definition

include(
    os.path.join(COMPONENTS_DIR_NAME, "applications.py"),
    os.path.join(COMPONENTS_DIR_NAME, "auth_validators.py"),
    os.path.join(COMPONENTS_DIR_NAME, "database.py"),
    os.path.join(COMPONENTS_DIR_NAME, "middleware.py"),
    os.path.join(COMPONENTS_DIR_NAME, "templates.py"),
)

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

LANGUAGE_CODE = 'ru'
LOCALE_PATHS = ['hierarchical_menu/locale']

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MENU_NAMESPACE = 'hierarchical_menu'
