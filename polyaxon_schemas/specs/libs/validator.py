# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.ops.container import ContainerConfig
from polyaxon_schemas.ops.environments import EnvironmentConfig
from polyaxon_schemas.ops.parallel import ParallelConfig


def validate_headers(spec, data):
    """Validates headers data and creates the config objects"""
    validated_data = {spec.VERSION: data[spec.VERSION], spec.KIND: data[spec.KIND]}

    if data.get(spec.TAGS):
        validated_data[spec.TAGS] = data[spec.TAGS]

    if data.get(spec.PARALLEL):
        validated_data[spec.HP_TUNING] = ParallelConfig.from_dict(data[spec.HP_TUNING])

    return validated_data


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
