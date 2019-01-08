from django.contrib.auth.models import Group


def register(admin_register):
    admin_register(Group)
