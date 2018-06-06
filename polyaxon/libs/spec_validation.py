from marshmallow.exceptions import ValidationError as MarshmallowValidationError
from rest_framework.exceptions import ValidationError

from django.core.exceptions import ValidationError as DjangoValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.polyaxonfile.specification import (
    BuildSpecification,
    ExperimentSpecification,
    GroupSpecification,
    NotebookSpecification,
    TensorboardSpecification,
    JobSpecification,
)
from polyaxon_schemas.hptuning import HPTuningConfig


def validate_experiment_spec_config(config, raise_for_rest=False):
    try:
        spec = ExperimentSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError) as e:
        message_error = 'Received non valid specification config. %s' % e
        if raise_for_rest:
            raise ValidationError(message_error)
        else:
            raise DjangoValidationError(message_error)

    return spec


def validate_group_spec_content(content, raise_for_rest=False):
    try:
        spec = GroupSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError) as e:
        message_error = 'Received non valid specification content. %s' % e
        if raise_for_rest:
            raise ValidationError(message_error)
        else:
            raise DjangoValidationError(message_error)

    return spec


def validate_group_hptuning_config(config, raise_for_rest=False):
    try:
        HPTuningConfig.from_dict(config)
    except MarshmallowValidationError as e:
        if raise_for_rest:
            raise ValidationError(e)
        else:
            raise DjangoValidationError(e)


def validate_notebook_spec_config(config, raise_for_rest=False):
    try:
        spec = NotebookSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError) as e:
        message_error = 'Received non valid notebook specification config. %s' % e
        if raise_for_rest:
            raise ValidationError(message_error)
        else:
            raise DjangoValidationError(message_error)

    return spec


def validate_tensorboard_spec_config(config, raise_for_rest=False):
    try:
        spec = TensorboardSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError) as e:
        message_error = 'Received non valid tensorboard specification config. %s' % e
        if raise_for_rest:
            raise ValidationError(message_error)
        else:
            raise DjangoValidationError(message_error)

    return spec


def validate_build_spec_config(config, raise_for_rest=False):
    try:
        spec = BuildSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError) as e:
        message_error = 'Received non valid build specification config. %s' % e
        if raise_for_rest:
            raise ValidationError(message_error)
        else:
            raise DjangoValidationError(message_error)

    return spec


def validate_job_spec_config(config, raise_for_rest=False):
    try:
        spec = JobSpecification.read(config)
    except (PolyaxonfileError, PolyaxonConfigurationError) as e:
        message_error = 'Received non valid job specification config. %s' % e
        if raise_for_rest:
            raise ValidationError(message_error)
        else:
            raise DjangoValidationError(message_error)

    return spec
