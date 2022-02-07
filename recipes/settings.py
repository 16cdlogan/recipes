"""
Django settings for recipes project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import ast
import json
import os
import re

from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get vars from .env files
SECRET_KEY = os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else 'INSECURE_STANDARD_KEY_SET_IN_ENV'

DEBUG = bool(int(os.getenv('DEBUG', True)))

SOCIAL_DEFAULT_ACCESS = bool(int(os.getenv('SOCIAL_DEFAULT_ACCESS', False)))
SOCIAL_DEFAULT_GROUP = os.getenv('SOCIAL_DEFAULT_GROUP', 'guest')

SPACE_DEFAULT_MAX_RECIPES = int(os.getenv('SPACE_DEFAULT_MAX_RECIPES', 0))
SPACE_DEFAULT_MAX_USERS = int(os.getenv('SPACE_DEFAULT_MAX_USERS', 0))
SPACE_DEFAULT_MAX_FILES = int(os.getenv('SPACE_DEFAULT_MAX_FILES', 0))
SPACE_DEFAULT_ALLOW_SHARING = bool(int(os.getenv('SPACE_DEFAULT_ALLOW_SHARING', True)))

INTERNAL_IPS = os.getenv('INTERNAL_IPS').split(',') if os.getenv('INTERNAL_IPS') else ['127.0.0.1']

# allow djangos wsgi server to server mediafiles
GUNICORN_MEDIA = bool(int(os.getenv('GUNICORN_MEDIA', True)))

REVERSE_PROXY_AUTH = bool(int(os.getenv('REVERSE_PROXY_AUTH', False)))

# default value for user preference 'comment'
COMMENT_PREF_DEFAULT = bool(int(os.getenv('COMMENT_PREF_DEFAULT', True)))
FRACTION_PREF_DEFAULT = bool(int(os.getenv('FRACTION_PREF_DEFAULT', False)))
KJ_PREF_DEFAULT = bool(int(os.getenv('KJ_PREF_DEFAULT', False)))
STICKY_NAV_PREF_DEFAULT = bool(int(os.getenv('STICKY_NAV_PREF_DEFAULT', True)))

# minimum interval that users can set for automatic sync of shopping lists
SHOPPING_MIN_AUTOSYNC_INTERVAL = int(os.getenv('SHOPPING_MIN_AUTOSYNC_INTERVAL', 5))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') if os.getenv('ALLOWED_HOSTS') else ['*']

CORS_ORIGIN_ALLOW_ALL = True

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"
ACCOUNT_LOGOUT_REDIRECT_URL = "index"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 365 * 60 * 24 * 60

CRISPY_TEMPLATE_PACK = 'bootstrap4'
DJANGO_TABLES2_TEMPLATE = 'cookbook/templates/generic/table_template.html'
DJANGO_TABLES2_PAGE_RANGE = 8

HCAPTCHA_SITEKEY = os.getenv('HCAPTCHA_SITEKEY', '')
HCAPTCHA_SECRET = os.getenv('HCAPTCHA_SECRET', '')

SHARING_ABUSE = bool(int(os.getenv('SHARING_ABUSE', False)))
SHARING_LIMIT = int(os.getenv('SHARING_LIMIT', 0))

ACCOUNT_SIGNUP_FORM_CLASS = 'cookbook.forms.AllAuthSignupForm'

TERMS_URL = os.getenv('TERMS_URL', '')
PRIVACY_URL = os.getenv('PRIVACY_URL', '')
IMPRINT_URL = os.getenv('IMPRINT_URL', '')
HOSTED = bool(int(os.getenv('HOSTED', False)))

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_prometheus',
    'django_tables2',
    'corsheaders',
    'django_filters',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'django_cleanup.apps.CleanupConfig',
    'webpack_loader',
    'django_js_reverse',
    'hcaptcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cookbook.apps.CookbookConfig',
    'treebeard',
]

SOCIAL_PROVIDERS = os.getenv('SOCIAL_PROVIDERS').split(',') if os.getenv('SOCIAL_PROVIDERS') else []
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
INSTALLED_APPS = INSTALLED_APPS + SOCIAL_PROVIDERS

ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 90
ACCOUNT_LOGOUT_ON_GET = True

try:
    SOCIALACCOUNT_PROVIDERS = ast.literal_eval(
        os.getenv('SOCIALACCOUNT_PROVIDERS') if os.getenv('SOCIALACCOUNT_PROVIDERS') else '{}')
except ValueError:
    SOCIALACCOUNT_PROVIDERS = json.loads(
        os.getenv('SOCIALACCOUNT_PROVIDERS').replace("'", '"') if os.getenv('SOCIALACCOUNT_PROVIDERS') else '{}')

SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'sessionid')

ENABLE_SIGNUP = bool(int(os.getenv('ENABLE_SIGNUP', False)))

ENABLE_METRICS = bool(int(os.getenv('ENABLE_METRICS', False)))

ENABLE_PDF_EXPORT = bool(int(os.getenv('ENABLE_PDF_EXPORT', False)))
EXPORT_FILE_CACHE_DURATION = int(os.getenv('EXPORT_FILE_CACHE_DURATION', 600))

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cookbook.helper.scope_middleware.ScopeMiddleware',
]

SORT_TREE_BY_NAME = bool(int(os.getenv('SORT_TREE_BY_NAME', False)))
DISABLE_TREE_FIX_STARTUP = bool(int(os.getenv('DISABLE_TREE_FIX_STARTUP', False)))

if bool(int(os.getenv('SQL_DEBUG', False))):
    MIDDLEWARE += ('recipes.middleware.SqlPrintingMiddleware',)

if ENABLE_METRICS:
    MIDDLEWARE += 'django_prometheus.middleware.PrometheusAfterMiddleware',

# Auth related settings
AUTHENTICATION_BACKENDS = []

# LDAP
LDAP_AUTH = bool(os.getenv('LDAP_AUTH', False))
if LDAP_AUTH:
    import ldap
    from django_auth_ldap.config import LDAPSearch
    AUTHENTICATION_BACKENDS.append('django_auth_ldap.backend.LDAPBackend')
    AUTH_LDAP_SERVER_URI = os.getenv('AUTH_LDAP_SERVER_URI')
    AUTH_LDAP_BIND_DN = os.getenv('AUTH_LDAP_BIND_DN')
    AUTH_LDAP_BIND_PASSWORD = os.getenv('AUTH_LDAP_BIND_PASSWORD')
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        os.getenv('AUTH_LDAP_USER_SEARCH_BASE_DN'),
        ldap.SCOPE_SUBTREE,
        os.getenv('AUTH_LDAP_USER_SEARCH_FILTER_STR', '(uid=%(user)s)'),
    )
    AUTH_LDAP_USER_ATTR_MAP = ast.literal_eval(os.getenv('AUTH_LDAP_USER_ATTR_MAP')) if os.getenv('AUTH_LDAP_USER_ATTR_MAP') else {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }
    AUTH_LDAP_ALWAYS_UPDATE_USER = bool(int(os.getenv('AUTH_LDAP_ALWAYS_UPDATE_USER', True)))
    AUTH_LDAP_CACHE_TIMEOUT = int(os.getenv('AUTH_LDAP_CACHE_TIMEOUT', 3600))
    if 'AUTH_LDAP_TLS_CACERTFILE' in os.environ:
        AUTH_LDAP_GLOBAL_OPTIONS = { ldap.OPT_X_TLS_CACERTFILE: os.getenv('AUTH_LDAP_TLS_CACERTFILE') }

AUTHENTICATION_BACKENDS += [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# django allauth site id
SITE_ID = int(os.getenv('ALLAUTH_SITE_ID', 1))

ACCOUNT_ADAPTER = 'cookbook.helper.AllAuthCustomAdapter'

if REVERSE_PROXY_AUTH:
    MIDDLEWARE.append('recipes.middleware.CustomRemoteUser')
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.RemoteUserBackend')

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

ROOT_URLCONF = 'recipes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'cookbook', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'cookbook.helper.context_processors.context_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'recipes.wsgi.application'

# Database
# Load settings from env files
if os.getenv('DATABASE_URL'):
    match = re.match(
        r'(?P<schema>\w+):\/\/(?P<user>[\w\d_-]+)(:(?P<password>[^@]+))?@(?P<host>[^:/]+)(:(?P<port>\d+))?(\/(?P<database>[\w\d\/\._-]+))?',
        os.getenv('DATABASE_URL')
    )
    settings = match.groupdict()
    schema = settings['schema']
    if schema.startswith('postgres'):
        engine = 'django.db.backends.postgresql'
    elif schema == 'sqlite':
        engine = 'django.db.backends.sqlite3'
    else:
        raise Exception("Unsupported database schema: '%s'" % schema)

    DATABASES = {
        'default': {
            'ENGINE': engine,
            'OPTIONS': ast.literal_eval(os.getenv('DB_OPTIONS')) if os.getenv('DB_OPTIONS') else {},
            'HOST': settings['host'],
            'PORT': settings['port'],
            'USER': settings['user'],
            'PASSWORD': settings['password'],
            'NAME': settings['database'],
            'CONN_MAX_AGE': 600,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE') if os.getenv('DB_ENGINE') else 'django.db.backends.sqlite3',
            'OPTIONS': ast.literal_eval(os.getenv('DB_OPTIONS')) if os.getenv('DB_OPTIONS') else {},
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'NAME': os.getenv('POSTGRES_DB') if os.getenv('POSTGRES_DB') else 'db.sqlite3',
            'CONN_MAX_AGE': 60,
        }
    }

# Local testing DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': 'localhost',
#         'PORT': 5432,
#         'USER': 'postgres',
#         'PASSWORD': 'postgres', # set to local pw
#         'NAME': 'postgres',
#         'CONN_MAX_AGE': 600,
#     }
# }

# SQLite testing DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'OPTIONS': ast.literal_eval(os.getenv('DB_OPTIONS')) if os.getenv('DB_OPTIONS') else {},
#         'NAME': 'db.sqlite3',
#         'CONN_MAX_AGE': 600,
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default',
    }
}

# Vue webpack settings
VUE_DIR = os.path.join(BASE_DIR, 'vue')

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(VUE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = os.getenv('TIMEZONE') if os.getenv('TIMEZONE') else 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('hy', _('Armenian ')),
    ('ca', _('Catalan')),
    ('cs', _('Czech')),
    ('nl', _('Dutch')),
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
    ('it', _('Italian')),
    ('lv', _('Latvian')),
    ('pl', _('Polish')),
    ('ru', _('Russian')),
    ('es', _('Spanish')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

SCRIPT_NAME = os.getenv('SCRIPT_NAME', '')
# path for django_js_reverse to generate the javascript file containing all urls. Only done because the default command (collectstatic_js_reverse) fails to update the manifest
JS_REVERSE_OUTPUT_PATH = os.path.join(BASE_DIR, "cookbook/static/django_js_reverse")
JS_REVERSE_SCRIPT_PREFIX = os.getenv('JS_REVERSE_SCRIPT_PREFIX', SCRIPT_NAME)

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

if os.getenv('S3_ACCESS_KEY', ''):
    DEFAULT_FILE_STORAGE = 'cookbook.helper.CustomStorageClass.CachedS3Boto3Storage'

    AWS_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', '')
    AWS_QUERYSTRING_AUTH = bool(int(os.getenv('S3_QUERYSTRING_AUTH', True)))
    AWS_QUERYSTRING_EXPIRE = int(os.getenv('S3_QUERYSTRING_EXPIRE', 3600))
    AWS_S3_SIGNATURE_VERSION = os.getenv('S3_SIGNATURE_VERSION', 's3v4')
    AWS_S3_REGION_NAME = os.getenv('S3_REGION_NAME', None)

    if os.getenv('S3_ENDPOINT_URL', ''):
        AWS_S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', '')

    MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
else:
    MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Serve static files with gzip
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEST_RUNNER = "cookbook.helper.CustomTestRunner.CustomTestRunner"

# settings for cross site origin (CORS)
# all origins allowed to support bookmarklet
# all of this may or may not work with nginx or other web servers
# TODO make this user configurable - enable or disable bookmarklets
# TODO since token auth is enabled - this all should be https by default
CORS_ORIGIN_ALLOW_ALL = True

# enable CORS only for bookmarklet api and only for posts, get and options
CORS_URLS_REGEX = r'^/api/bookmarklet-import.*$'
CORS_ALLOW_METHODS = ['GET', 'OPTIONS', 'POST']
# future versions of django will make undeclared default django.db.models.BigAutoField which will force migrations on all models
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = bool(int(os.getenv('EMAIL_USE_TLS', False)))
EMAIL_USE_SSL = bool(int(os.getenv('EMAIL_USE_SSL', False)))
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
ACCOUNT_EMAIL_SUBJECT_PREFIX = os.getenv('ACCOUNT_EMAIL_SUBJECT_PREFIX', '[Tandoor Recipes] ')  # allauth sender prefix

