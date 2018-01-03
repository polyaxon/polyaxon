# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.utils import config

REGISTRATION_SUPERUSER_VALIDATION_WORKFLOW = '0'
EMAIL_VALIDATION_WORKFLOW = '1'

REGISTRATION_WORKFLOW = REGISTRATION_SUPERUSER_VALIDATION_WORKFLOW

USERS_MINIMUM_PASSWORD_LENGTH = config.get_int('POLYAXON_PASSWORD_LENGTH')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': USERS_MINIMUM_PASSWORD_LENGTH,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
