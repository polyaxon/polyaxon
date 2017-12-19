# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.core.exceptions import ValidationError
from polyaxon_schemas.exceptions import PolyaxonfileError, PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification


def validate_spec_content(content):
    try:
        spec = GroupSpecification.read(content)
    except (PolyaxonfileError, PolyaxonConfigurationError):
        raise ValidationError('Received non valid specification content.')

    if spec.is_local:
        raise ValidationError('Received specification content for a local environment run.')

    return spec
