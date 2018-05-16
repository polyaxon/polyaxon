# -*- coding: utf-8 -*-
import django_auth_ldap
from django.dispatch import receiver
from django_auth_ldap.backend import populate_user

@receiver(populate_user)
def populate_user(sender, **kwargs):
    user = kwargs['user']
    user.email = '%s@ldap-users.com' % user.username
