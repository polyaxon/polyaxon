from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from django.core.exceptions import ValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.polyaxonfile.specification import (
    ExperimentSpecification,
    GroupSpecification,
    PluginSpecification
)
from polyaxon_schemas.settings import SettingsConfig


def validate_experiment_spec_config(config):
    try:
        spec = ExperimentSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid specification config.')

    return spec


def validate_group_spec_content(content):
    try:
        spec = GroupSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid specification content.')

    return spec


def validate_group_params_config(config):
    try:
        SettingsConfig.from_dict(config)
    except MarshmallowValidationError as e:
        raise ValidationError(e)


def validate_plugin_spec_config(config):
    try:
        spec = PluginSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid tensorboard specification config.')

    return spec
