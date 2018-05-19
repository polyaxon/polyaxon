import logging

from django.dispatch import receiver
from django_auth_ldap.backend import populate_user

from django.conf import settings

logger = logging.getLogger('polyaxon.users.auth_ldap')


@receiver(populate_user)
def populate_user_handler(sender, **kwargs):
    user = kwargs['user']
    ldap_user = user.ldap_user

    # populate user with default email to prevent validation error
    if not user.email:
        try:
            value = ldap_user.attrs['mail'][0]
        except LookupError:
            logger.warning("%s does not have a value for the attribute %s",
                           ldap_user.dn, 'mail')
            user.email = '%s@%s' % (user.username, settings.DEFAULT_EMAIL_DOMAIN)
        else:
            user.email = value
