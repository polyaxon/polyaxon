# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

"""
WSGI config for search project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polyaxon.settings')

application = get_wsgi_application()
