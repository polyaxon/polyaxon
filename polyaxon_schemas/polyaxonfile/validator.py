# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.run_exec import RunExecConfig
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.models import ModelConfig
from polyaxon_schemas.polyaxonfile.specification import Specification
from polyaxon_schemas.settings import SettingsConfig, EnvironmentConfig
from polyaxon_schemas.train import TrainConfig
from polyaxon_schemas.project import ProjectConfig


def validate_headers(data):
    """Validates headers data and creates the config objects"""
    validated_data = {
        Specification.VERSION: data[Specification.VERSION],
        Specification.PROJECT: ProjectConfig.from_dict(data[Specification.PROJECT]),
    }
    if data.get(Specification.SETTINGS):
        validated_data[Specification.SETTINGS] = SettingsConfig.from_dict(
            data[Specification.SETTINGS])

    return validated_data


def validate_matrix(data):
    """Validates matrix data and creates the config objects"""
    if not data:
        return None

    validate_data = {}
    for key, value in six.iteritems(data):
        validate_data[key] = MatrixConfig.from_dict(value)

    return validate_data


def validate(data):
    """Validates the data and creates the config objects"""
    validated_data = {}

    def add_validated_section(section, config):
        if data.get(section):
            validated_data[section] = config.from_dict(data[section])

    add_validated_section(Specification.ENVIRONMENT, EnvironmentConfig)
    add_validated_section(Specification.RUN_EXEC, RunExecConfig)
    add_validated_section(Specification.MODEL, ModelConfig)
    add_validated_section(Specification.TRAIN, TrainConfig)
    add_validated_section(Specification.EVAL, EvalConfig)

    return validated_data
