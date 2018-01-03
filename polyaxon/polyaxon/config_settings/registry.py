# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.utils import config

REGISTRY_USER = config.get_string('POLYAXON_REGISTRY_USER', is_optional=True)
REGISTRY_PASSWORD = config.get_string('POLYAXON_REGISTRY_PASSWORD', is_optional=True)
REGISTRY_HOST = config.get_string('POLYAXON_REGISTRY_HOST', is_optional=True)
