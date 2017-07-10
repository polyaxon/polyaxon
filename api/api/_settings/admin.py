# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config

email_from = config.get_string('EMAIL_FROM')

admin_name = config.get_string('ADMIN_NAME')
admin_mail = config.get_string('ADMIN_MAIL')


ADMINS = (
    (admin_name, admin_mail),
)

MANAGERS = ADMINS
