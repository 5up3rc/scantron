"""
Django settings for scantron project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import environ

# JSON-based secrets module.
# ------------------------------------------------------------------------------
import json
import os

from django.core.exceptions import ImproperlyConfigured

ROOT_DIR = environ.Path(__file__) - 3  # (master/config/settings/base.py - 3 = scantron/)
APPS_DIR = ROOT_DIR.path('django_scantron')  # scantron/master/django_scantron

# scantron_secrets.json sits in the root of the scantron folder.
with open(os.path.join(str(ROOT_DIR), 'scantron_secrets.json')) as fh:
    secrets_environment = os.environ["DJANGO_SETTINGS_MODULE"].split('.')[-1]
    print("[*] Loading [ {} ] scantron_secrets.json".format(secrets_environment))
    secrets = json.loads(fh.read())


def get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return explicit exception.
    """
    try:
        if os.environ["DJANGO_SETTINGS_MODULE"] == "config.settings.local":
            return secrets['local'][setting]
        else:
            return secrets['production'][setting]

    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# ------------------------------------------------------------------------------

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    'rest_framework',  # Django REST Framework
    'rest_framework.authtoken',  # Enable token authentication for Django REST Framework
    'django_filters',  # Search filters for Django REST Framework
    'rest_framework_swagger',  # API documentation and support framework
    'recurrence',  # Used to configure periodic scans
    # 'django_baker'  # Django baker is used to create CRUD files for each model.
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'django_scantron',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Admin""", 'admin@localhost'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DATABASE_NAME'),
        'HOST': get_secret('DATABASE_HOST'),
        'PORT': get_secret('DATABASE_PORT'),
        'USER': get_secret('DATABASE_USER'),
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
    }
}

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Chicago'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

SESSION_COOKIE_AGE = 36000  # 10 hours

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = '/var/www/static'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static/scantron')),  # master/django_scantron/static/scantron/
    str(ROOT_DIR.path('static')),  # webapp/static/
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# MEDIA_ROOT =

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
# MEDIA_URL = ''

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'

# Your common stuff: Below this line define 3rd party library settings
# -------------------------------------------------------------------------------
# Django REST Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ),
    # Token Authentication.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
