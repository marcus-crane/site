import configparser
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load in API keys and other secrets
config = configparser.ConfigParser()
config.read(BASE_DIR + '/keys.ini')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'supersecretkey123pleasedontsteal'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'thingsimade',
    'base',
    'blog',
    'contact',
    'projects',
    'reviews', 
    'stats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thingsimade.urls'

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

WSGI_APPLICATION = 'thingsimade.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Pacific/Auckland'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

# API Keys
LAST_FM = config['keys']['lastfm']
RECAPTCHA_PUBLIC = config['keys']['recaptcha_public']
RECAPTCHA_PRIVATE = config['keys']['recaptcha_private']
STEAM = config['keys']['steam']
TMDB = config['keys']['tmdb']
TRAKT = config['keys']['trakt']

# Production settings
if os.environ['USER'] == 'sentry':
    STATIC_URL = 'https://static.thingsima.de/'
    DEBUG = False
    ALLOWED_HOSTS = ['thingsima.de', 'www.thingsima.de']
    SECRET_KEY = config['keys']['django']

# Email settings
EMAIL_HOST = config['email']['host']
EMAIL_HOST_USER = config['email']['user']
EMAIL_HOST_PASSWORD = config['email']['password']
EMAIL_PORT = config['email']['port']
EMAIL_USE_SSL = True
