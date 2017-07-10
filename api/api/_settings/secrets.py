# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config

SECRET_KEY = config.get_string('SECRET_KEY')
