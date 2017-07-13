# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config

DEBUG = config.get_boolean('DJANGO_DEBUG')

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

WSGI_APPLICATION = 'api.wsgi.application'
TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', u'English'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

INTERNAL_IPS = ('127.0.0.1',)
APPEND_SLASH = True

USERS_MINIMUM_PASSWORD_LENGTH = config.get_int('PASSWORD_LENGTH')

ROOT_URLCONF = 'api.urls'

# user management
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_TIMEOUT_DAYS = 3
INVITATION_TIMEOUT_DAYS = 30

SESSION_COOKIE_AGE = 24 * 60 * 60  # 24 hours
SESSION_COOKIE_HTTPONLY = True


DATABASES = {
    'default': {
        'ENGINE': config.get_string('DB_ENGINE'),
        'NAME': config.get_string('DB_NAME'),
        'USER': config.get_string('DB_USER'),
        'PASSWORD': config.get_string('DB_PASSWORD'),
        'HOST': config.get_string('DB_HOST'),
        'PORT': config.get_string('DB_PORT'),
        'ATOMIC_REQUESTS': True
    }
}

LIST_TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
]

JS_DEBUG = config.get_boolean('JS_DEBUG')

if JS_DEBUG:
    def js_debug_processor(request):
        return {'js_debug': True}

    LIST_TEMPLATE_CONTEXT_PROCESSORS += ('api.settings.js_debug_processor', )


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': config.get_boolean('DJANGO_TEMPLATE_DEBUG', is_optional=True) or DEBUG,
            'context_processors': LIST_TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]


SHORTNAME_BLACKLIST = (
    'admin',
    'dashboard',
    'index',
    'log',
    'logs',
    'metric',
    'metrics',
    'perspectives',
    'portfolio',
)
