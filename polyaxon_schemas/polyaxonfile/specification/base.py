# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import six
import os

from marshmallow import ValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile import constants
from polyaxon_schemas.polyaxonfile import validator
from polyaxon_schemas.polyaxonfile import reader
from polyaxon_schemas.polyaxonfile.parser import Parser
from polyaxon_schemas.polyaxonfile.utils import cached_property, get_vol_path
from polyaxon_schemas.operators import ForConfig, IfConfig
from polyaxon_schemas.settings import RunTypes
from polyaxon_schemas.utils import to_list


@six.add_metaclass(abc.ABCMeta)
class BaseSpecification(object):
    """Base abstract specification for plyaxonfiles and configurations."""

    MAX_VERSION = 1.0  # Min Polyaxonfile specification version this CLI supports
    MIN_VERSION = 1.0  # Max Polyaxonfile specification version this CLI supports

    VERSION = 'version'
    PROJECT = 'project'
    SETTINGS = 'settings'
    MATRIX = 'matrix'
    DECLARATIONS = 'declarations'
    ENVIRONMENT = 'environment'
    RUN_EXEC = 'run'
    MODEL = 'model'
    TRAIN = 'train'
    EVAL = 'eval'

    SECTIONS = (
        VERSION, PROJECT, ENVIRONMENT, MATRIX, DECLARATIONS, SETTINGS, RUN_EXEC, MODEL, TRAIN, EVAL
    )

    HEADER_SECTIONS = (
        VERSION, PROJECT, SETTINGS
    )

    GRAPH_SECTIONS = (
        MODEL, TRAIN, EVAL
    )

    REQUIRED_SECTIONS = (
        VERSION, PROJECT
    )

    OPERATORS = {
        ForConfig.IDENTIFIER: ForConfig,
        IfConfig.IDENTIFIER: IfConfig,
    }

    def __init__(self, values):
        self._values = to_list(values)

        self._data = reader.read(self._values)
        Parser.check_data(spec=self, data=self._data)
        headers = Parser.get_headers(spec=self, data=self._data)
        try:
            self._headers = validator.validate_headers(spec=self, data=headers)
        except ValidationError as e:
            raise PolyaxonConfigurationError(e)
        parsed_data = Parser.parse(self, self._data, None)
        self._validated_data = validator.validate(spec=self, data=parsed_data)
        self._parsed_data = parsed_data

    @classmethod
    def read(cls, filepaths):
        if isinstance(filepaths, cls):
            return filepaths
        return cls(filepaths)

    @property
    def values(self):
        return self._values

    @cached_property
    def data(self):
        return self._data

    @cached_property
    def headers(self):
        return self._headers

    @cached_property
    def parsed_data(self):
        return self._parsed_data

    @cached_property
    def version(self):
        return self.headers[self.VERSION]

    @cached_property
    def project(self):
        return self.headers[self.PROJECT]

    @cached_property
    def settings(self):
        return self.headers.get(self.SETTINGS, None)

    @cached_property
    def run_type(self):
        return self.settings.run_type if self.settings else RunTypes.KUBERNETES

    @cached_property
    def log_level(self):
        if self.settings and self.settings.logging:
            return self.settings.logging.level
        return 'INFO'

    @cached_property
    def is_local(self):
        return self.run_type == RunTypes.LOCAL

    @cached_property
    def is_minikube(self):
        return self.run_type == RunTypes.MINIKUBE

    @cached_property
    def is_kubernetes(self):
        return self.run_type == RunTypes.KUBERNETES

    @cached_property
    def project_path(self):
        def get_path():
            project_path = None
            if self.settings:
                project_path = self.settings.logging.path

            if project_path:
                return project_path

            if self.run_type == RunTypes.LOCAL:
                return '/tmp/plx_logs/' + self.project.name

            return os.path.join(get_vol_path(constants.LOGS_VOLUME, self.run_type),
                                self.project.name)

        return get_path()
