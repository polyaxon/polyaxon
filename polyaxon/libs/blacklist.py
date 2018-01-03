# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.core.exceptions import ValidationError

NAME_BLACKLIST = [
    'user',
    'users',
    'admin',
    'admins',
    'experiment',
    'experiments',
    'experiment_group',
    'experiment_groups',
    'project',
    'projects',
    'api',
    'polyaxon',
    'dashboard',
    'index',
    'log',
    'logs',
    'metric',
    'metrics',
    'perspectives',
    'portfolio',
    'public',
    'revision',
    'revisions',
    'version',
    'versions',
    'support',
    'tryout',
    'repo',
    'repos',
    'cluster',
    'event',
    'events',
]


def validate_blacklist_name(name):
    """Validates slug name against a blacklist"""
    if name is None:
        raise ValidationError(_('A short name must be supplied.'))

    if name in NAME_BLACKLIST:
        raise ValidationError('The short name is a reserved word or already taken.')
