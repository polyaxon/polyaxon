from django.core.exceptions import ValidationError
from polyaxon_schemas.exceptions import PolyaxonfileError, PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification, PluginSpecification


def validate_run_type(spec):
    if spec.is_local:
        raise ValidationError('Received specification content for a local environment run.')


def validate_spec_content(content):
    try:
        spec = GroupSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid specification content.')

    validate_run_type(spec)

    return spec


def validate_tensorboard_spec_content(content):
    try:
        spec = PluginSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid tensorboard specification content.')

    validate_run_type(spec)

    return spec
