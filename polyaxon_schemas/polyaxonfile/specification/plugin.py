# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.specification.build import BuildSpecification


class NotebookSpecification(BuildSpecification):
    """The polyaxonfile specification for notebooks.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._NOTEBOOK  # pylint:disable=protected-access

    def _extra_validation(self):
        try:
            super(NotebookSpecification, self)._extra_validation()
        except PolyaxonConfigurationError:
            raise PolyaxonConfigurationError(
                'NotebookSpecification must contain a valid `build` section.')


class TensorboardSpecification(BuildSpecification):
    """The polyaxonfile specification for tensorboard.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._TENSORBOARD  # pylint:disable=protected-access

    def _extra_validation(self):
        try:
            super(TensorboardSpecification, self)._extra_validation()
        except PolyaxonConfigurationError:
            raise PolyaxonConfigurationError(
                'TensorboardSpecification must contain a valid `build` section.')
