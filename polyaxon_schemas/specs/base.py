# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import copy
import six

from collections import Mapping

import rhea

from hestia.cached_property import cached_property
from hestia.list_utils import to_list
from marshmallow import EXCLUDE, ValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.ops import params as ops_params
from polyaxon_schemas.ops.environments.pods import EnvironmentConfig
from polyaxon_schemas.ops.operators import ForConfig, IfConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.libs import validator
from polyaxon_schemas.specs.libs.parser import Parser


@six.add_metaclass(abc.ABCMeta)
class BaseSpecification(object):
    """Base abstract specification for plyaxonfiles and configurations."""

    _SPEC_KIND = None

    MAX_VERSION = 1  # Max Polyaxonfile specification version this CLI supports
    MIN_VERSION = 1  # Min Polyaxonfile specification version this CLI supports

    VERSION = 'version'
    KIND = 'kind'
    LOGGING = 'logging'
    NAME = 'name'
    DESCRIPTION = 'description'
    TAGS = 'tags'
    INPUTS = 'inputs'
    OUTPUTS = 'outputs'
    BACKEND = 'backend'
    FRAMEWORK = 'framework'
    HP_TUNING = 'hptuning'
    DECLARATIONS = 'declarations'
    PARAMS = 'params'
    ENVIRONMENT = 'environment'
    RUN = 'run'
    BUILD = 'build'

    SECTIONS = (
        VERSION, KIND, NAME, DESCRIPTION, LOGGING, TAGS,
        INPUTS, OUTPUTS, DECLARATIONS, PARAMS,
        BACKEND, FRAMEWORK, ENVIRONMENT,
        HP_TUNING, BUILD, RUN
    )

    STD_PARSING_SECTIONS = (BACKEND, FRAMEWORK, ENVIRONMENT, LOGGING, TAGS)
    OP_PARSING_SECTIONS = (BUILD, RUN, )

    HEADER_SECTIONS = (
        VERSION, KIND, NAME, DESCRIPTION, LOGGING, TAGS,
    )

    GRAPH_SECTIONS = []

    REQUIRED_SECTIONS = (
        VERSION, KIND
    )

    POSSIBLE_SECTIONS = (
        VERSION, KIND, LOGGING, TAGS, NAME, DESCRIPTION, INPUTS, OUTPUTS
    )

    OPERATORS = {
        ForConfig.IDENTIFIER: ForConfig,
        IfConfig.IDENTIFIER: IfConfig,
    }

    ENVIRONMENT_CONFIG = EnvironmentConfig
    CONFIG = None

    def __init__(self, values):
        self._values = to_list(values)

        try:
            self._data = rhea.read(self._values)
        except rhea.RheaError as e:
            raise PolyaxonConfigurationError(e)
        try:
            self._config_data = self._get_config(self._data)
        except ValidationError as e:
            raise PolyaxonfileError(e)
        self.check_data()
        headers = Parser.get_headers(spec=self, data=self._data)
        try:
            self._headers = validator.validate_headers(spec=self, data=headers)
        except ValidationError as e:
            raise PolyaxonConfigurationError(e)
        self._parsed_data = None
        self._validated_data = None
        self._config = None
        self._extra_validation()

    def _extra_validation(self):
        pass

    @cached_property
    def config(self):
        return self._config

    @cached_property
    def raw_config(self):
        return self._config_data

    def _get_config(self, data):
        config = self.CONFIG.from_dict(copy.deepcopy(data))
        ops_params.validate_params(params=config.params,
                                   inputs=config.inputs,
                                   outputs=config.outputs,
                                   is_template=False,
                                   is_run=True)
        return config

    def parse_data(self, context=None):
        return self.apply_context(context=context)

    def apply_context(self, context=None):
        context = context or {}
        params = self._config_data.get_params(context=context)
        parsed_data = Parser.parse(self, self._config_data, params, None)
        self._config = self._get_config(parsed_data)
        self._parsed_data = parsed_data
        return parsed_data

    @classmethod
    def check_version(cls, data):
        if cls.VERSION not in data:
            raise PolyaxonfileError("The Polyaxonfile `version` must be specified.")
        if not cls.MIN_VERSION <= data[cls.VERSION] <= cls.MAX_VERSION:
            raise PolyaxonfileError(
                "The Polyaxonfile's version specified is not supported by your current CLI."
                "Your CLI support Polyaxonfile versions between: {} <= v <= {}."
                "You can run `polyaxon upgrade` and "
                "check documentation for the specification.".format(
                    cls.MIN_VERSION, cls.MAX_VERSION))

    @classmethod
    def check_kind(cls, data):
        if cls.KIND not in data:
            raise PolyaxonfileError("The Polyaxonfile `kind` must be specified.")

        if data[cls.KIND] not in kinds.KINDS:
            raise PolyaxonfileError(
                "The Polyaxonfile with kind `{}` is not a supported value.".format(data[cls.KIND]))

    def check_data(self, data=None):
        data = data or self._data
        self.check_version(data)
        self.check_kind(data)
        if data[self.KIND] != self._SPEC_KIND:
            raise PolyaxonfileError(
                "The specification used `{}` is incompatible with the kind `{}`.".format(
                    self.__class__.__name__, data[self.KIND]))
        for key in set(six.iterkeys(data)) - set(self.SECTIONS):
            raise PolyaxonfileError(
                "Unexpected section `{}` in Polyaxonfile version `{}`. "
                "Please check the Polyaxonfile specification "
                "for this version.".format(key, data[self.VERSION]))

        for key in set(six.iterkeys(data)) - set(self.POSSIBLE_SECTIONS):
            raise PolyaxonfileError(
                "Unexpected section `{}` for specification kind `{}` version `{}`. "
                "Please check the Polyaxonfile specification "
                "for this version.".format(key, self._SPEC_KIND, data[self.VERSION]))

        for key in self.REQUIRED_SECTIONS:
            if key not in data:
                raise PolyaxonfileError("{} is a required section for a valid Polyaxonfile".format(
                    key))

    def patch(self, values):
        values = [self._parsed_data] + to_list(values)
        spec = self.read(values=values)
        spec.apply_context()
        return spec

    @classmethod
    def get_kind(cls, data):
        cls.check_kind(data=data)
        return data[cls.KIND]

    @classmethod
    def read(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values)

    @cached_property
    def is_experiment(self):
        return self.kind == kinds.EXPERIMENT

    @cached_property
    def is_group(self):
        return self.kind == kinds.GROUP

    @cached_property
    def is_job(self):
        return self.kind == kinds.JOB

    @cached_property
    def is_notebook(self):
        return self.kind == kinds.NOTEBOOK

    @cached_property
    def is_tensorboard(self):
        return self.kind == kinds.TENSORBOARD

    @cached_property
    def is_build(self):
        return self.kind == kinds.BUILD

    @cached_property
    def is_pipeline(self):
        return self.kind == kinds.PIPELINE

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
    def raw_data(self):
        return '{}'.format(self._data)

    @cached_property
    def version(self):
        return self.headers[self.VERSION]

    @cached_property
    def kind(self):
        return self.headers[self.KIND]

    @cached_property
    def logging(self):
        return self.headers.get(self.LOGGING, None)

    @cached_property
    def log_level(self):
        if self.logging:
            return self.logging.level
        return 'INFO'

    @cached_property
    def tags(self):
        tags = self.headers.get(self.TAGS, None)
        return list(set(tags)) if tags else None


class EnvironmentSpecificationMixin(object):

    @cached_property
    def environment(self):
        return self._config_data.environment

    @cached_property
    def resources(self):
        return self.environment.resources if self.environment else None

    @cached_property
    def artifact_refs(self):
        return self.environment.artifact_refs if self.environment else None

    @cached_property
    def data_refs(self):
        return self.environment.data_refs if self.environment else None

    @cached_property
    def secret_refs(self):
        return self.environment.secret_refs if self.environment else None

    @cached_property
    def config_map_refs(self):
        return self.environment.config_map_refs if self.environment else None

    @cached_property
    def node_selector(self):
        return self.environment.node_selector if self.environment else None

    @cached_property
    def affinity(self):
        return self.environment.affinity if self.environment else None

    @cached_property
    def tolerations(self):
        return self.environment.tolerations if self.environment else None

    @cached_property
    def outputs(self):
        return self.environment.outputs if self.environment else None

    @cached_property
    def max_restarts(self):
        return self.environment.max_restarts if self.environment else None


class BaseRunSpecification(BaseSpecification, EnvironmentSpecificationMixin):
    """The polyaxonfile specification for build jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = kinds.BUILD

    HEADER_SECTIONS = BaseSpecification.HEADER_SECTIONS + (BaseSpecification.BACKEND, )

    POSSIBLE_SECTIONS = BaseSpecification.POSSIBLE_SECTIONS + (
        BaseSpecification.ENVIRONMENT, BaseSpecification.BUILD, BaseSpecification.BACKEND,
    )

    @cached_property
    def build(self):
        return self.config.build

    @classmethod
    def create_specification(cls,  # pylint:disable=arguments-differ
                             build_config,
                             to_dict=True):
        from polyaxon_schemas.ops.build_job import BuildConfig

        if isinstance(build_config, BuildConfig):
            b_config = build_config.to_light_dict()
        elif isinstance(build_config, Mapping):
            # Since the objective is to create the build spec from other specs
            # we drop any extra attrs
            b_config = BuildConfig.from_dict(build_config, unknown=EXCLUDE)
            b_config = b_config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        specification = {
            cls.VERSION: 1,
            cls.KIND: cls._SPEC_KIND,
            cls.BUILD: b_config,
        }

        if to_dict:
            return specification
        return cls.read(specification)
