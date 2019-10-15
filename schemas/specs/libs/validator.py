# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from schemas.exceptions import PolyaxonfileError
from schemas.ops.container import ContainerConfig
from schemas.ops.environments import EnvironmentConfig


def validate(spec, data):
    """Validates the data and creates the config objects"""
    data = copy.deepcopy(data)
    validated_data = {}

    def validate_keys(section, config, section_data):
        extra_args = [
            key for key in section_data.keys() if key not in config.SCHEMA().fields
        ]
        if extra_args:
            raise PolyaxonfileError(
                "Extra arguments passed for `{}`: {}".format(section, extra_args)
            )

    def add_validated_section(section, config):
        if data.get(section):
            section_data = data[section]
            validate_keys(section=section, config=config, section_data=section_data)
            validated_data[section] = config.from_dict(section_data)

    add_validated_section(spec.ENVIRONMENT, EnvironmentConfig)
    add_validated_section(spec.CONTAINER, ContainerConfig)

    return validated_data
