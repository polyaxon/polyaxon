import os
import django
from django.conf import settings


if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polyaxon.settings')
    django.setup()
