IS_PRODUCTION = False
DEBUG = True
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rh3w_ft#nkxcd^ldz6rx9b+yd8-+t6@-64@yy05ap7+=s0*hqt'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [

    "admin_interface",
    "colorfield",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_admin_listfilter_dropdown',

    # Third party apps
	'rest_framework',
	'django_filters',
	'rest_framework.authtoken',
	'corsheaders',
    'import_export',
    'authentication',
    'Agency',
    'transaction',
    "wallet"

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
	'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'mtrans.urls'

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

WSGI_APPLICATION = 'mtrans.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if IS_PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mtrans',
            'USER': 'root',
            'PASSWORD': 'MTRANS1234',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



LANGUAGES = (
    ('en', ('English')),
    ('fr', ('French')),
    ('it', ('Italiano')),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'


if DEBUG:
    STATICFILES_DIRS = (
        BASE_DIR / 'static',
    )
else: 
    STATIC_ROOT = 'static/'

MEDIA_ROOT = BASE_DIR / 'media'

X_FRAME_OPTIONS = 'ALLOWALL'
CORS_ORIGIN_ALLOW_ALL = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework.authentication.BasicAuthentication',
		#'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.TokenAuthentication',
	],
	'DEFAULT_FILTER_BACKENDS': [
		'django_filters.rest_framework.DjangoFilterBackend',
		'rest_framework.filters.SearchFilter',
		'rest_framework.filters.OrderingFilter',
	],
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
	'PAGE_SIZE': 100,
}