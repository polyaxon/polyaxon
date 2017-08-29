# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.models import ModelConfig
from polyaxon_schemas.settings import SettingsConfig
from polyaxon_schemas.train import TrainConfig
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.project import ProjectConfig


def validate(data):
    """Validates the data and creates the config objects"""
    if 'project' not in data:
        raise PolyaxonfileError("The Polyaxonfile must contain a project section.")

    if 'model' not in data:
        raise PolyaxonfileError("The Polyaxonfile must contain a model section.")

    validated_data = {
        'version': data['version'],
        'project': ProjectConfig.from_dict(data['project']),
        'model': ModelConfig.from_dict(data['model'])
    }
    if data.get('settings'):
        validated_data['settings'] = SettingsConfig.from_dict(data['settings'])

    if data.get('train'):
        validated_data['train'] = TrainConfig.from_dict(data['train'])

    if data.get('eval'):
        validated_data['eval'] = EvalConfig.from_dict(data['eval'])

    return validated_data
