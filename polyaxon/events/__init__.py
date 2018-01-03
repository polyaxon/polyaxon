# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import django
from django.conf import settings


if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polyaxon.settings')
    django.setup()
