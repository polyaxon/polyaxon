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
from polyaxon_schemas.pkg import SCHEMA_VERSION
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.libs.parser import Parser


class EnvironmentSpecificationMixin(object):
    @property
    def environment(self):
        return self.config.environment

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

    @property
    def auth_context(self):
        return self.environment.auth if self.environment else None

    @property
    def docker_context(self):
        return self.environment.docker if self.environment else None

    @property
    def shm_context(self):
        return self.environment.shm if self.environment else None

    @property
    def registry(self):
        return self.environment.registry if self.environment else None

    @property
    def outputs(self):
        return self.environment.outputs if self.environment else None

    @property
    def logs(self):
        return self.environment.logs if self.environment else None


class InitSpecificationMixin(object):
    @property
    def init(self):
        return self.config.init

    @property
    def repos(self):
        return self.init.repos if self.init else None

    @property
    def repos_names(self):
        return self._get_refs_names(self.repos)

    @property
    def repos_by_names(self):
        return self._get_refs_by_names(self.repos)

    @property
    def build_context(self):
        return self.init.build if self.init else None

    @property
    def init_artifacts(self):
        return self.init.artifacts if self.init else None

    @property
    def init_artifacts_names(self):
        return self._get_refs_names(self.init_artifacts)

    @property
    def init_artifacts_by_names(self):
        return self._get_refs_by_names(self.init_artifacts)


class MountsSpecificationMixin(object):
    @property
    def mounts(self):
        return self.config.mounts

    @property
    def mounts_name(self):
        return self.mounts.name if self.mounts else None

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
        return self.mounts.artifacts if self.mounts else None

    @property
    def artifacts_names(self):
        return self._get_refs_names(self.artifacts)

    @property
    def artifacts_by_names(self):
        return self._get_refs_by_names(self.artifacts)

    @property
    def secrets(self):
        return self.mounts.secrets if self.mounts else None

    @property
    def secrets_names(self):
        return self._get_refs_names(self.secrets)

    @property
    def secrets_by_names(self):
        return self._get_refs_by_names(self.secrets)

    @property
    def config_maps(self):
        return self.mounts.config_maps if self.mounts else None

    @property
    def config_maps_names(self):
        return self._get_refs_names(self.config_maps)

    @property
    def config_maps_by_names(self):
        return self._get_refs_by_names(self.config_maps)


class ParallelSpecificationMixin(object):
    @property
    def parallel(self):
        return self.config.parallel

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
        return self.config.termination

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
    InitSpecificationMixin,
    MountsSpecificationMixin,
    TerminationSpecificationMixin,
    ParallelSpecificationMixin,
):
    """Base abstract specification for plyaxonfiles and configurations."""

    _SPEC_KIND = None

    MAX_VERSION = (
        SCHEMA_VERSION
    )  # Max Polyaxonfile specification version this CLI supports
    MIN_VERSION = (
        SCHEMA_VERSION
    )  # Min Polyaxonfile specification version this CLI supports

    VERSION = "version"
    KIND = "kind"
    NAME = "name"
    DESCRIPTION = "description"
    TAGS = "tags"
    PROFILE = "profile"
    NOCACHE = "nocache"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    PARAMS = "params"
    ENVIRONMENT = "environment"
    TERMINATION = "termination"
    INIT = "init"
    MOUNTS = "mounts"
    CONTAINER = "container"
    PARALLEL = "parallel"
    REPLICA_SPEC = "replica_spec"
    PORTS = "ports"
    TEMPLATES = "templates"
    OPS = "ops"
    SCHEDULE = "schedule"
    DEPENDENCIES = "dependencies"
    TRIGGER = "trigger"
    CONDITIONS = "conditions"

    SECTIONS = (
        VERSION,
        KIND,
        NAME,
        DESCRIPTION,
        TAGS,
        INPUTS,
        OUTPUTS,
        PARAMS,
        PROFILE,
        NOCACHE,
        ENVIRONMENT,
        TERMINATION,
        INIT,
        MOUNTS,
        CONTAINER,
        PARALLEL,
        REPLICA_SPEC,
        PORTS,
        TEMPLATES,
        OPS,
        SCHEDULE,
        DEPENDENCIES,
        TRIGGER,
        CONDITIONS,
    )

    PARSING_SECTIONS = (
        PROFILE,
        NOCACHE,
        ENVIRONMENT,
        TERMINATION,
        INIT,
        MOUNTS,
        CONTAINER,
        REPLICA_SPEC,
        PORTS,
    )
    OP_PARSING_SECTIONS = (TEMPLATES, OPS, SCHEDULE, DEPENDENCIES, TRIGGER, CONDITIONS)

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
            self._config = self.CONFIG.from_dict(copy.deepcopy(self.data))
        except (ValidationError, TypeError) as e:
            raise PolyaxonfileError(e)
        self.check_data()
        self._extra_validation()

    def _extra_validation(self):
        pass

    @property
    def config(self):
        return self._config

    def _parse(self, params):
        params = params or {}
        parsed_data = Parser.parse(self, self.config, params)
        return self.read(parsed_data)

    def validate_params(self, params=None, context=None, is_template=True, check_runs=False):
        try:
            return ops_params.validate_params(
                inputs=self.config.inputs,
                outputs=self.config.outputs,
                params=params,
                context=context,
                is_template=is_template,
                check_runs=check_runs
            )
        except ValidationError as e:
            raise PolyaxonfileError(e)

    def apply_params(self, params=None, context=None):
        context = context or {}
        validated_params = self.validate_params(
            params=params, context=context, is_template=False, check_runs=True
        )
        if not validated_params:
            return

        params = {}
        for param in validated_params:
            params[param.name] = param

        def set_io(io):
            if not io:
                return
            for i in io:
                if i.name in params:
                    i.value = params[i.name].value
                    i.is_optional = True

        set_io(self.config.inputs)
        set_io(self.config.outputs)

    def apply_context(self):
        params = self.validate_params(is_template=False, check_runs=True)

        for param in params:
            if param.entity_ref:
                raise PolyaxonfileError(
                    "apply_context recieved a non-resolved "
                    "ref param `{}` with value `{}`".format(param.name, param.value)
                )

        params = {param.name: param for param in params}
        return self._parse(params)

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
        values = [self.data] + to_list(values)
        return self.read(values=values)

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
    def data_dump(self):
        return json.dumps(self._data)

    @property
    def config_dump(self):
        return json.dumps(self.config.to_light_dict())

    @property
    def version(self):
        return self.config.version

    @property
    def kind(self):
        return self.config.kind

    @property
    def name(self):
        return self.config.name

    @property
    def description(self):
        return self.config.description

    @property
    def tags(self):
        return self.config.tags

    @property
    def profile(self):
        return self.config.profile

    @property
    def nocache(self):
        return self.config.nocache

    @property
    def container(self):
        return self.config.container
