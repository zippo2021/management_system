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
CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = (
   	'management_system',
	'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'django.contrib.humanize',  # Required for elapsed time formatting
    'crispy_forms',
    'registration',
    'customuseradmin',
    'markdown_deux',  # Required for Knowledgebase item formatting
    'helpdesk', 
    'bootstrap_toolkit',
    'markdown_deux',    
    'dashboard.teacher',
    'dashboard.regular',
    'dashboard.mentor',
    'dashboard.observer',
    'dashboard.event_worker',
    'dashboard.userdata',
    'dashboard.common_profile',
	'events.comments',
    'events.events_admin',
    'events.events_manage',
    'events.notes',
    'events.raps',
    'events.study_groups',
    'events.journal',
    'events.price_groups',
    'events.tickets',
    'export',
    'schools',
    'search',
    'user_manager',
    'news',
    'feedback',
)

MIDDLEWARE_CLASSES = (  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.SubdomainMiddleware',
)

DATABASE_ROUTERS = ['routers.SubdomainRouter',
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
	},

	'sub1': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'sub1',
        'USER': 'user1',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
	},
	
	'sub2': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'sub2',
        'USER': 'user2',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
	}
}

# Django-registration

ACCOUNT_ACTIVATION_DAYS = 1
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'managtest@yandex.ru'
EMAIL_HOST_PASSWORD = 'qwerty2021'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'managtest@yandex.ru'
LOGIN_REDIRECT_URL = '/news/main/'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    )

TEMPLATE_CONTEXT_PROCESSORS = (
            global_settings.TEMPLATE_CONTEXT_PROCESSORS +
            ('django.core.context_processors.request',
			 'context_processors.organisation_settings_processor',
			 'context_processors.permission_translation_processor',
             'context_processors.events_processor',
             'context_processors.documents_translation_processor',
             'context_processors.user_permissions_processor',
            )
     )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,"media")
MEDIA_URL = '/media/'
MAX_UPLOAD_SIZE = 1024*1024
CONTENT_TYPES = ["image/jpeg","image/png"]
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

'''
UPLOADCARE = {
    'pub_key': '40f8c675ce99f1fa7ab6',
    'secret': 'd44ce3444b9a9218c6e9',
}
'''

FORMAT_MODULE_PATH = 'management_system.formats'

EVENT_ATTACHMENTS_DIR = os.path.join(BASE_DIR, "files/events/")
EVENT_EMAIL_TEMPLATES_DIR = os.path.join(BASE_DIR, "email_templates/events/")
