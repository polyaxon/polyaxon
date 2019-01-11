from django.contrib.admin import site
from django.contrib.auth.models import Group


def register(admin_register):
    site.unregister(Group)
