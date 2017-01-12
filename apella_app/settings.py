"""
Django settings for apella_app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(DATA_DIR, ...)
import os
DATA_DIR = os.path.abspath(os.getcwd())
RESOURCES_DIR = os.path.join(DATA_DIR, 'resources')
SETTINGS_DIR = os.environ.get('APELLA_SETTINGS_DIR', '/etc/apella')
SETTINGS_FILE = 'settings.conf'

MEDIA_ROOT = '/tmp'
OLD_APELLA_MEDIA_ROOT = '/tmp'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4#yxh34pn@&8(8)pa6#70h6e#jl2vo-uf@9w1ex!)7r4n%da#6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apella',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'apella_app.urls'

WSGI_APPLICATION = 'apella_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/apella.sqlite3'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
AUTH_USER_MODEL = 'apella.ApellaUser'

START_DATE_END_DATE_INTERVAL = 30
LANGUAGES = {'el', 'en'}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
API_HOST = None  # The host the app is served from
API_PREFIX = 'apella/'
TOKEN_LOGIN_URL = '/apella/ui/auth/login'
TOKEN_REGISTER_URL = '/apella/ui/auth/register/professor'
AUTH_USER_MODEL = 'apella.ApellaUser'
DOWNLOAD_FILE_URL = '/apella/ui/auth/login'

START_DATE_END_DATE_INTERVAL = 30
LANGUAGES = {'el', 'en'}
POSITION_CODE_PREFIX = 'APP'

CONFIG_FILE = 'apella.apimas'

DJOSER = {
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'ACTIVATION_URL': 'apella/ui/auth/login#activate={uid}|{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'apella/ui/auth/login#reset={uid}|{token}'
}

APELLA_LEGACY_ACADEMIC_LOGIN_URL = None

SETTINGS_PATH = os.path.join(SETTINGS_DIR, SETTINGS_FILE)

if not os.path.isfile(SETTINGS_PATH):
    m = "Cannot find settings file {0!r}. Consider using APELLA_SETTINGS_DIR "
    m += "environment variable to set a custom path for settings.conf file."
    m = m.format(SETTINGS_PATH)
    raise RuntimeError(m)

LOGGING = None

execfile(SETTINGS_PATH)

# Logging configuration
if not LOGGING:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s\
                %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(DATA_DIR, 'apella.log'),
                'formatter': 'verbose'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'apella': {
                'handlers': ['console', 'file'],
                'level': 'INFO'
            }
        }
    }


if not DEBUG and not API_HOST:
    raise Exception("API_HOST setting is required when DEBUG is set to False.")
