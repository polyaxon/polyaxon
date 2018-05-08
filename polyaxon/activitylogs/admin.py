from django.contrib.admin import site

from .models import ActivityLog

site.register(ActivityLog)
