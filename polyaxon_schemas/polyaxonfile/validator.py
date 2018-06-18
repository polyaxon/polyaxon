# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon_schemas.build import BuildConfig
from polyaxon_schemas.environments import EnvironmentConfig
from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.hptuning import HPTuningConfig
from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.models import ModelConfig
from polyaxon_schemas.run_exec import RunConfig
from polyaxon_schemas.train import TrainConfig


def validate_headers(spec, data):
    """Validates headers data and creates the config objects"""
    validated_data = {
        spec.VERSION: data[spec.VERSION],
        spec.KIND: data[spec.KIND],
    }

    if data.get(spec.LOGGING):
        validated_data[spec.LOGGING] = LoggingConfig.from_dict(
            data[spec.LOGGING])

    if data.get(spec.TAGS):
        validated_data[spec.TAGS] = data[spec.TAGS]

    if data.get(spec.HP_TUNING):
        validated_data[spec.HP_TUNING] = HPTuningConfig.from_dict(
            data[spec.HP_TUNING])

    return validated_data


def validate(spec, data):
    """Validates the data and creates the config objects"""
    data = copy.deepcopy(data)
    validated_data = {}

    def add_validated_section(section, config):
        if data.get(section):
            validated_data[section] = config.from_dict(data[section])

    add_validated_section(spec.ENVIRONMENT, EnvironmentConfig)
    add_validated_section(spec.BUILD, BuildConfig)
    add_validated_section(spec.RUN, RunConfig)
    add_validated_section(spec.MODEL, ModelConfig)
    add_validated_section(spec.TRAIN, TrainConfig)
    add_validated_section(spec.EVAL, EvalConfig)

    return validated_data
