# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_client.exceptions import PolyaxonException


def validate_config(config, config_schema):
    if isinstance(config, Mapping):
        return config_schema.from_dict(config)
    elif not isinstance(config, config_schema):
        raise PolyaxonException(
            'Received an invalid config. '
            'Expects a Mapping or an instance of `{}`.'.format(config_schema.__name__))

    return config
