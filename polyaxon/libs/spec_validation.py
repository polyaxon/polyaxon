from django.core.exceptions import ValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.polyaxonfile.specification import (
    ExperimentSpecification,
    GroupSpecification,
    PluginSpecification
)


def validate_experiment_spec_content(content):
    try:
        spec = ExperimentSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid specification content.')

    return spec


def validate_group_spec_content(content):
    try:
        spec = GroupSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid specification content.')

    return spec


def validate_tensorboard_spec_content(content):
    try:
        spec = PluginSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid tensorboard specification content.')

    return spec
