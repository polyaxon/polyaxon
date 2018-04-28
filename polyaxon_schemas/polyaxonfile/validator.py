# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon_schemas.environments import EnvironmentConfig
from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.models import ModelConfig
from polyaxon_schemas.run_exec import RunExecConfig
from polyaxon_schemas.settings import SettingsConfig
from polyaxon_schemas.train import TrainConfig


def validate_headers(spec, data):
    """Validates headers data and creates the config objects"""
    validated_data = {
        spec.VERSION: data[spec.VERSION],
        spec.KIND: data[spec.KIND],
    }
    if data.get(spec.SETTINGS):
        validated_data[spec.SETTINGS] = SettingsConfig.from_dict(
            data[spec.SETTINGS])

    return validated_data


def validate(spec, data):
    """Validates the data and creates the config objects"""
    data = copy.deepcopy(data)
    validated_data = {}

    def add_validated_section(section, config):
        if data.get(section):
            validated_data[section] = config.from_dict(data[section])

    add_validated_section(spec.ENVIRONMENT, EnvironmentConfig)
    add_validated_section(spec.RUN_EXEC, RunExecConfig)
    add_validated_section(spec.MODEL, ModelConfig)
    add_validated_section(spec.TRAIN, TrainConfig)
    add_validated_section(spec.EVAL, EvalConfig)

    return validated_data
