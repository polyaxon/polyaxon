# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import copy
import json
import six

import rhea

from hestia.list_utils import to_list
from marshmallow import ValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.ops import params as ops_params
from polyaxon_schemas.ops.operators import ForConfig, IfConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.libs import validator
from polyaxon_schemas.specs.libs.parser import Parser


class EnvironmentSpecificationMixin(object):
    @property
    def environment(self):
        return self._config_data.environment

    @property
    def environment_name(self):
        return self.environment.name if self.environment else None

    @property
    def resources(self):
        return self.environment.resources if self.environment else None

    @property
    def labels(self):
        return self.environment.labels if self.environment else None

    @property
    def annotations(self):
        return self.environment.annotations if self.environment else None

    @property
    def node_selector(self):
        return self.environment.node_selector if self.environment else None

    @property
    def affinity(self):
        return self.environment.affinity if self.environment else None

    @property
    def tolerations(self):
        return self.environment.tolerations if self.environment else None

    @property
    def security_context(self):
        return self.environment.security_context if self.environment else None

    @property
    def service_account(self):
        return self.environment.service_account if self.environment else None

    @property
    def env_vars(self):
        return self.environment.env_vars if self.environment else None

    @property
    def image_pull_secrets(self):
        return self.environment.image_pull_secrets if self.environment else None

    @property
    def log_level(self):
        return self.environment.log_level if self.environment else None


class ContextsSpecificationMixin(object):
    @property
    def contexts(self):
        return self._config_data.contexts

    @property
    def contexts_name(self):
        return self.contexts.name if self.contexts else None

    @staticmethod
    def _get_refs_names(refs):
        if refs:
            return [r.name for r in refs]

    @staticmethod
    def _get_refs_by_names(refs):
        if refs:
            return {r.name: r for r in refs}

    @property
    def artifacts(self):
        return self.contexts.artifacts if self.contexts else None

    @property
    def artifacts_names(self):
        return self._get_refs_names(self.artifacts)

    @property
    def artifacts_by_names(self):
        return self._get_refs_by_names(self.artifacts)

    @property
    def secrets(self):
        return self.contexts.secrets if self.contexts else None

    @property
    def secrets_names(self):
        return self._get_refs_names(self.secrets)

    @property
    def secrets_by_names(self):
        return self._get_refs_by_names(self.secrets)

    @property
    def config_maps(self):
        return self.contexts.config_maps if self.contexts else None

    @property
    def config_maps_names(self):
        return self._get_refs_names(self.config_maps)

    @property
    def config_maps_by_names(self):
        return self._get_refs_by_names(self.config_maps)

    @property
    def repos(self):
        return self.contexts.repos if self.contexts else None

    @property
    def repos_names(self):
        return self._get_refs_names(self.repos)

    @property
    def repos_by_names(self):
        return self._get_refs_by_names(self.repos)

    @property
    def registry(self):
        return self.contexts.registry if self.contexts else None

    @property
    def outputs(self):
        return self.contexts.outputs if self.contexts else None

    @property
    def build_context(self):
        return self.contexts.build if self.contexts else None

    @property
    def auth_context(self):
        return self.contexts.auth if self.contexts else None

    @property
    def docker_context(self):
        return self.contexts.docker if self.contexts else None

    @property
    def shm_context(self):
        return self.contexts.shm if self.contexts else None


class ParallelSpecificationMixin(object):
    @property
    def parallel(self):
        return self._config_data.parallel

    @property
    def early_stopping(self):
        early_stopping = None
        if self.parallel:
            early_stopping = self.parallel.early_stopping
        return early_stopping or []

    @property
    def parallel_algorithm(self):
        return self.parallel.algorithm if self.parallel else None

    @property
    def parallel_algorithm_kind(self):
        return self.parallel_algorithm.kind if self.parallel_algorithm else None

    @property
    def concurrency(self):
        concurrency = None
        if self.parallel:
            concurrency = self.parallel.concurrency
        return concurrency or 1


class TerminationSpecificationMixin(object):
    @property
    def termination(self):
        return self._config_data.termination

    @property
    def termination_name(self):
        return self.termination.name if self.termination else None

    @property
    def max_retries(self):
        return self.termination.max_retries if self.termination else None

    @property
    def timeout(self):
        return self.termination.timeout if self.termination else None

    @property
    def restart_policy(self):
        return self.termination.restart_policy if self.termination else None

    @property
    def ttl(self):
        return self.termination.ttl if self.termination else None


@six.add_metaclass(abc.ABCMeta)
class BaseSpecification(
    EnvironmentSpecificationMixin,
    ContextsSpecificationMixin,
    TerminationSpecificationMixin,
    ParallelSpecificationMixin,
):
    """Base abstract specification for plyaxonfiles and configurations."""

    _SPEC_KIND = None

    MAX_VERSION = 0.6  # Max Polyaxonfile specification version this CLI supports
    MIN_VERSION = 0.6  # Min Polyaxonfile specification version this CLI supports

    VERSION = "version"
    KIND = "kind"
    NAME = "name"
    DESCRIPTION = "description"
    TAGS = "tags"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    PARAMS = "params"
    ENVIRONMENT = "environment"
    TERMINATION = "termination"
    CONTEXTS = "contexts"
    CONTAINER = "container"
    PARALLEL = "parallel"
    REPLICA_SPEC = "replica_spec"
    PORTS = "ports"
    TEMPLATES = "templates"
    OPS = "ops"
    SCHEDULE = "schedule"
    CONCURRENCY = "concurrency"

    SECTIONS = (
        VERSION,
        KIND,
        NAME,
        DESCRIPTION,
        TAGS,
        INPUTS,
        OUTPUTS,
        PARAMS,
        ENVIRONMENT,
        TERMINATION,
        CONTEXTS,
        CONTAINER,
        PARALLEL,
        REPLICA_SPEC,
        PORTS,
        TEMPLATES,
        OPS,
        SCHEDULE,
        CONCURRENCY,
    )

    PARSING_SECTIONS = (
        ENVIRONMENT,
        TERMINATION,
        CONTEXTS,
        CONTAINER,
        REPLICA_SPEC,
        PORTS,
    )
    OP_PARSING_SECTIONS = (TEMPLATES, OPS, SCHEDULE, CONCURRENCY)

    HEADER_SECTIONS = (VERSION, KIND, NAME, DESCRIPTION, TAGS)

    REQUIRED_SECTIONS = (VERSION, KIND)

    OPERATORS = {ForConfig.IDENTIFIER: ForConfig, IfConfig.IDENTIFIER: IfConfig}

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
        self._config = None
        self._extra_validation()

    def _extra_validation(self):
        pass

    @property
    def config(self):
        return self._config

    @property
    def raw_config(self):
        return self._config_data

    def _get_config(self, data):
        config = self.CONFIG.from_dict(copy.deepcopy(data))
        ops_params.validate_params(
            params=config.params,
            inputs=config.inputs,
            outputs=config.outputs,
            is_template=False,
            is_run=True,
        )
        return config

    def parse_data(self, context=None):
        return self.apply_context(context=context)

    def apply_context(self, context=None):
        context = context or {}
        params = self._config_data.get_params(context=context)
        parsed_data = Parser.parse(self, self._config_data, params)
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
                    cls.MIN_VERSION, cls.MAX_VERSION
                )
            )

    @classmethod
    def check_kind(cls, data):
        if cls.KIND not in data:
            raise PolyaxonfileError("The Polyaxonfile `kind` must be specified.")

        if data[cls.KIND] not in kinds.KINDS:
            raise PolyaxonfileError(
                "The Polyaxonfile with kind `{}` is not a supported value.".format(
                    data[cls.KIND]
                )
            )

    def check_data(self, data=None):
        data = data or self._data
        self.check_version(data)
        self.check_kind(data)
        if data[self.KIND] != self._SPEC_KIND:
            raise PolyaxonfileError(
                "The specification used `{}` is incompatible with the kind `{}`.".format(
                    self.__class__.__name__, data[self.KIND]
                )
            )
        for key in set(six.iterkeys(data)) - set(self.SECTIONS):
            raise PolyaxonfileError(
                "Unexpected section `{}` in Polyaxonfile version `{}`. "
                "Please check the Polyaxonfile specification "
                "for this version.".format(key, data[self.VERSION])
            )

        for key in self.REQUIRED_SECTIONS:
            if key not in data:
                raise PolyaxonfileError(
                    "{} is a required section for a valid Polyaxonfile".format(key)
                )

    def patch(self, values):
        values = [self._parsed_data] + to_list(values)
        spec = self.read(values=values)
        spec.apply_context()
        return spec

    @classmethod
    def get_kind(cls, data):
        cls.check_kind(data=data)
        return data[cls.KIND]

    @staticmethod
    def check_kind_job(kind):
        return kind == kinds.JOB

    @staticmethod
    def check_kind_service(kind):
        return kind == kinds.SERVICE

    @staticmethod
    def check_kind_pipeline(kind):
        return kind == kinds.PIPELINE

    @classmethod
    def read(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values)

    @property
    def is_job(self):
        return self.check_kind_job(self.kind)

    @property
    def is_service(self):
        return self.check_kind_notebook(self.kind)

    @property
    def is_pipeline(self):
        return self.check_kind_pipeline(self.kind)

    @property
    def values(self):
        return self._values

    @property
    def data(self):
        return self._data

    @property
    def headers(self):
        return self._headers

    @property
    def parsed_data(self):
        return self._parsed_data

    @property
    def raw_data(self):
        return json.dumps(self._data)

    @property
    def version(self):
        return self.headers[self.VERSION]

    @property
    def kind(self):
        return self.headers[self.KIND]

    @property
    def name(self):
        return self.headers[self.NAME]

    @property
    def description(self):
        return self.headers[self.DESCRIPTION]

    @property
    def tags(self):
        return self.headers.get(self.TAGS, None)

    @property
    def params(self):
        return self.parsed_data.get(self.PARAMS, None)

    @property
    def container(self):
        return self.config.container
