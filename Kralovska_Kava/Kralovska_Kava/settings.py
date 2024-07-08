import os
from google.oauth2 import service_account
from django.utils.translation import gettext_lazy as _ 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['35.208.49.205', "kavakral.store"]


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'rest_framework',
    'manager',
    'home',
    'reservation',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Kralovska_Kava.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Kralovska_Kava.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),  # Или IP-адрес вашего сервера PostgreSQL
        'PORT': os.getenv('DB_PORT'),       # Порт, на котором работает PostgreSQL (по умолчанию 5432)
    }
}

AUTH_USER_MODEL = 'manager.Manager'

AUTHENTICATION_BACKENDS = [
    'manager.backends.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 1,  # минимальная длина пароля
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('cs', _('Czech')),
    ('uk', _('Ukrainian')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGE_COOKIE_NAME = 'django_language'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Путь к файлу ключа учетной записи службы
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, os.getenv('GCP_KEY_FILE_PATH'))  # Укажите правильный путь к файлу ключа
)

# Установите использование Google Cloud Storage по умолчанию для файлов
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Укажите имя вашего Google Cloud Storage bucket
GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')

# При необходимости укажите собственный домен для медиафайлов (например, если используете CDN)
GS_CUSTOM_ENDPOINT = os.getenv('GS_CUSTOM_ENDPOINT')

# Установите URL для медиафайлов
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

# Опционально, установите управление кэшем для медиафайлов
# GS_DEFAULT_ACL = 'publicRead'  # Сделать файлы публичными по умолчанию
GS_FILE_OVERWRITE = False      # Не перезаписывать файлы с одинаковыми именами
GS_CACHE_CONTROL = 'max-age=86400'  # Кэшировать файлы на 1 день

# Настройка для статических файлов, если нужно
# STATIC_URL = '/static/'
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'

# Определяем, что STATIC_ROOT не нужен, так как статические файлы хранятся в облаке
STATIC_ROOT = ''

# Не указываем дополнительные директории для сбора статических файлов
STATICFILES_DIRS = []

# STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

