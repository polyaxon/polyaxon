# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config


class RoutingKeys(object):
    EVENTS_NAMESPACE = config.get_string('POLYAXON_ROUTING_KEYS_EVENTS_NAMESPACE')
    EVENTS_RESOURCES = config.get_string('POLYAXON_ROUTING_KEYS_EVENTS_RESOURCES')
    EVENTS_JOB_STATUSES = config.get_string('POLYAXON_ROUTING_KEYS_EVENTS_JOB_STATUSES')
    LOGS_SIDECARS = config.get_string('POLYAXON_ROUTING_KEYS_LOGS_SIDECARS')

