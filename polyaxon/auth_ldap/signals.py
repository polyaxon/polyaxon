# -*- coding: utf-8 -*-
import logging

from django.dispatch import receiver
from django_auth_ldap.backend import populate_user

logger = logging.getLogger('polyaxon.auth_ldap')

DEFAULT_EMAIL_DOMAIN = 'polyaxon-ldap-users.com'

@receiver(populate_user)
def populate_user(sender, **kwargs):
    user = kwargs['user']
    ldap_user = user.ldap_user

    # populate user with default email to prevent validation error
    if not user.email:
        try:
            value = ldap_user.attrs['mail'][0]
        except LookupError:
            logger.warning("{} does not have a value for the attribute {}".format(ldap_user.dn, 'mail'))
            user.email = '%s@%s' % (user.username, DEFAULT_EMAIL_DOMAIN)
        else:
            user.email = value
