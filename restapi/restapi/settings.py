from pathlib import Path
from datetime import timedelta
# import django_crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&1l4fw48=h#_6q!o=1f2^uja=6_5(os@rp=a1!2v#)gccxoc1p'

DEBUG = True

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'accounts',
    'token_nfts',
    'django_cron',
]

CRON_CLASSES = [
    # ...
]

# CRONJOBS = [
#     ('* * * * *', 'cron.example_job'),
#     ('* * * * *', 'restapi.cron.example_job')
# ]

# Token lifetime format/duration
F_ACCESS_TOKEN = "minutes"
T_ACCESS_TOKEN = 5
F_REFRESH_TOKEN = "minutes"
T_REFRESH_TOKEN = 15

SIMPLE_JWT = {
    # NOTE: Access tokens should live no longer than 5 minutes,
    # after that set a new access token using the refresh token
    # FIXME: Set to 5 minutes in production, 1 minute is only for testing purposes 
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=T_ACCESS_TOKEN),
    # TODO: Estimate the best lifetime for refresh tokens
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=T_REFRESH_TOKEN),
    'ROTATE_REFRESH_TOKENS': True,
    # NOTE: Only refresh tokens are blacklisted
    'BLACKLIST_AFTER_ROTATION': True
}

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTH_USER_MODEL = 'accounts.UserAccount'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'restapi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
