"""
Django settings for management_system project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ht5h_2#dttw)+-s$lkmurmv^6%8i@%i)gznwzl#x2!j&-=0h7='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Required for elapsed time formatting
    'registration',
    'customuseradmin',
    'markdown_deux',  # Required for Knowledgebase item formatting
    'helpdesk', 
    'bootstrap_toolkit',
    'bootstrapform',
    'markdown_deux',    
    'dashboard.teacher',
    'dashboard.regular',
    'events.comments',
    'events.events_admin',
    'events.notes',
    'events.raps',
    'events.study_groups',
    'events.price_groups',
    'events.tickets',
    'define_user',
    'export',
    'schools',
    'search',
)

MIDDLEWARE_CLASSES = (  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.KeywordMiddleware',
)

DATABASE_ROUTERS = ['routers.CoreRouter',
		    'routers.KeywordRouter',
]

ROOT_URLCONF = 'management_system.urls'

WSGI_APPLICATION = 'management_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'management_system',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Django-registration

ACCOUNT_ACTIVATION_DAYS = 2
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'regtest2014@gmail.com'
EMAIL_HOST_PASSWORD = 'curebadbreath'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'regtest2014@gmail.com'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    )

TEMPLATE_CONTEXT_PROCESSORS = (
            global_settings.TEMPLATE_CONTEXT_PROCESSORS +
            ('django.core.context_processors.request',)
     )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
