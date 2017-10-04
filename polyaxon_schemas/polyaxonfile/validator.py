# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.models import ModelConfig
from polyaxon_schemas.polyaxonfile.specification import Specification
from polyaxon_schemas.settings import SettingsConfig, EnvironmentConfig
from polyaxon_schemas.train import TrainConfig
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.project import ProjectConfig


def validate(data):
    """Validates the data and creates the config objects"""
    for section in Specification.REQUIRED_SECTIONS:

        if section not in data:
            raise PolyaxonfileError("The Polyaxonfile must contain a {} section.".format(section))

    validated_data = {
        Specification.VERSION: data[Specification.VERSION],
        Specification.PROJECT: ProjectConfig.from_dict(data[Specification.PROJECT]),
        Specification.MODEL: ModelConfig.from_dict(data[Specification.MODEL])
    }

    def add_validated_section(section, config):
        if data.get(section):
            validated_data[section] = config.from_dict(data[section])

    add_validated_section(Specification.SETTINGS, SettingsConfig)
    add_validated_section(Specification.ENVIRONMENT, EnvironmentConfig)
    add_validated_section(Specification.TRAIN, TrainConfig)
    add_validated_section(Specification.EVAL, EvalConfig)

    return validated_data
