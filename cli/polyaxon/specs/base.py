#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8
from __future__ import absolute_import, division, print_function

import abc
import copy
import six

from collections import namedtuple

import ujson

from hestia.list_utils import to_list
from marshmallow import ValidationError

from polyaxon import kinds
from polyaxon.config_reader import reader
from polyaxon.exceptions import (
    PolyaxonException,
    PolyaxonfileError,
    PolyaxonSchemaError,
)
from polyaxon.pkg import SCHEMA_VERSION
from polyaxon.schemas.polyflow import params as ops_params
from polyaxon.schemas.polyflow.operators import ForConfig, IfConfig
from polyaxon.schemas.polyflow.parallel import ParallelMixin
from polyaxon.schemas.polyflow.params import ParamSpec
from polyaxon.schemas.polyflow.run import RunMixin
from polyaxon.specs.libs.parser import Parser
from polyaxon.types import types


class MetaInfoSpec(
    namedtuple("MetaInfoSpec", "service concurrency run_kind parallel_kind"),
    RunMixin,
    ParallelMixin,
):
    @classmethod
    def get(cls, service=False, concurrency=None, run_kind=None, parallel_kind=None):
        return cls(
            service=service,
            concurrency=concurrency,
            run_kind=run_kind,
            parallel_kind=parallel_kind,
        )

    def get_run_kind(self):
        return self.run_kind

    def get_parallel_kind(self):
        return self.parallel_kind

    def to_dict(self):
        return dict(self._asdict())


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

    @property
    def init_container(self):
        return self.environment.init_container if self.environment else None

    @property
    def sidecar_container(self):
        return self.environment.sidecar_container if self.environment else None


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


class RunSpecificationMixin(RunMixin):
    @property
    def run(self):
        return self.config.run

    @property
    def run_early_stopping(self):
        early_stopping = None
        if self.has_dag_run:
            early_stopping = self.run.early_stopping
        return early_stopping or []

    @property
    def run_kind(self):
        return self.run.kind if self.run else None

    def get_run_kind(self):
        return self.run_kind

    @property
    def run_concurrency(self):
        concurrency = None
        if self.has_dag_run:
            concurrency = self.run.concurrency
        return concurrency


class ParallelSpecificationMixin(ParallelMixin):
    @property
    def parallel(self):
        return self.config.parallel

    @property
    def parallel_early_stopping(self):
        early_stopping = None
        if self.parallel:
            early_stopping = self.parallel.early_stopping
        return early_stopping or []

    @property
    def parallel_kind(self):
        return self.parallel.kind if self.parallel else None

    def get_parallel_kind(self):
        return self.parallel_kind

    @property
    def parallel_concurrency(self):
        concurrency = None
        if self.parallel:
            concurrency = self.parallel.concurrency
        return concurrency


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


class ScheduleSpecificationMixin(object):
    @property
    def schedule(self):
        return self.config.schedule

    @property
    def schedule_kind(self):
        return self.schedule.kind if self.schedule else None

    @property
    def schedule_start_at(self):
        return self.schedule.start_at if self.schedule else None

    @property
    def schedule_end_at(self):
        return self.schedule.end_at if self.schedule else None

    @property
    def schedule_frequency(self):
        return self.schedule.frequency if self.schedule else None

    @property
    def schedule_cron(self):
        return self.schedule.cron if self.schedule else None

    @property
    def schedule_depends_on_past(self):
        return self.schedule.depends_on_past if self.schedule else None


@six.add_metaclass(abc.ABCMeta)
class BaseSpecification(
    EnvironmentSpecificationMixin,
    InitSpecificationMixin,
    MountsSpecificationMixin,
    TerminationSpecificationMixin,
    RunSpecificationMixin,
    ParallelSpecificationMixin,
    ScheduleSpecificationMixin,
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
    QUEUE = "queue"
    NOCACHE = "nocache"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    PARAMS = "params"
    ENVIRONMENT = "environment"
    TERMINATION = "termination"
    INIT = "init"
    MOUNTS = "mounts"
    RUN = "run"
    PARALLEL = "parallel"
    SERVICE = "service"
    OPERATIONS = "operations"
    COMPONENTS = "components"
    SCHEDULE = "schedule"
    DEPENDENCIES = "dependencies"
    TRIGGER = "trigger"
    CONDITIONS = "conditions"
    SKIP_ON_UPSTREAM_SKIP = "skip_on_upstream_skip"
    COMPONENT_REF = "component_ref"
    COMPONENT = "component"

    SECTIONS = (
        VERSION,
        KIND,
        NAME,
        DESCRIPTION,
        TAGS,
        PARAMS,
        PROFILE,
        NOCACHE,
        ENVIRONMENT,
        TERMINATION,
        INIT,
        MOUNTS,
        PARALLEL,
        SERVICE,
        OPERATIONS,
        SCHEDULE,
        DEPENDENCIES,
        TRIGGER,
        CONDITIONS,
        SKIP_ON_UPSTREAM_SKIP,
        COMPONENT_REF,
        COMPONENT,
        INPUTS,
        OUTPUTS,
        RUN,
    )

    PARSING_SECTIONS = (
        PROFILE,
        NOCACHE,
        ENVIRONMENT,
        TERMINATION,
        SCHEDULE,
        INIT,
        MOUNTS,
        SERVICE,
    )
    OP_PARSING_SECTIONS = (OPERATIONS, SCHEDULE, DEPENDENCIES, TRIGGER, CONDITIONS)

    REQUIRED_SECTIONS = (VERSION, KIND)

    OPERATORS = {ForConfig.IDENTIFIER: ForConfig, IfConfig.IDENTIFIER: IfConfig}

    CONFIG = None

    def __init__(self, values):
        self._values = to_list(values)

        self._data = reader.read(
            [{"kind": self._SPEC_KIND, "version": SCHEMA_VERSION}] + self._values
        )
        try:
            self._config = self.CONFIG.from_dict(copy.deepcopy(self.data))
        except (ValidationError, TypeError) as e:
            raise PolyaxonfileError(
                "Received a non valid config `{}`: `{}`".format(self._SPEC_KIND, e)
            )
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

    def validate_params(
        self, params=None, context=None, is_template=True, check_runs=False
    ):
        try:
            return ops_params.validate_params(
                inputs=self.config.inputs,
                outputs=self.config.outputs,
                params=params,
                context=context,
                is_template=is_template,
                check_runs=check_runs,
            )
        except ValidationError as e:
            raise PolyaxonfileError("Params validation error: `{}`".format(e))

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

    def _apply_run_context(self):
        params = self.validate_params(is_template=False, check_runs=True)

        for param in params:
            if param.entity_ref:
                raise PolyaxonfileError(
                    "apply_context recieved a non-resolved "
                    "ref param `{}` with value `{}`".format(param.name, param.value)
                )

        params = {param.name: param for param in params}
        return self._parse(params)

    def _apply_dag_context(self):
        self.run.process_dag()
        self.run.validate_dag()
        self.run.process_components(self.config.inputs)
        return self

    def apply_context(self):
        if self.has_dag_run:
            return self._apply_dag_context()
        else:
            return self._apply_run_context()

    def apply_run_contexts(self, contexts=None):
        if self.has_pipeline:
            raise PolyaxonSchemaError(
                "This method is not allowed on this specification."
            )
        params = self.validate_params(is_template=False, check_runs=True)
        params = {param.name: param for param in params}
        contexts = contexts or {}
        contexts = {
            k: ParamSpec(
                name=k,
                value=v,
                iotype=types.STR,
                entity=None,
                entity_ref=None,
                entity_value=None,
                is_flag=False,
            )
            for k, v in six.iteritems(contexts)
        }
        params.update(contexts)
        parsed_data = Parser.parse_run(self, self.data, params)
        return self.read(parsed_data)

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
    def check_kind_op(kind):
        return kind == kinds.OP

    @staticmethod
    def check_kind_component(kind):
        return kind == kinds.COMPONENT

    @classmethod
    def read(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values)

    @property
    def is_op(self):
        return self.check_kind_op(self.kind)

    @property
    def is_component(self):
        return self.check_kind_component(self.kind)

    @property
    def has_service(self):
        return self.config.service is not None

    @property
    def has_pipeline(self):
        return self.has_dag_run or self.parallel

    @property
    def meta_info(self):
        return MetaInfoSpec.get(
            service=self.has_service,
            # We prioritize parallel over run because parallel manages run (even dags)
            concurrency=(
                self.parallel_concurrency
                if self.parallel_concurrency is not None
                else self.run_concurrency
            ),
            run_kind=self.run_kind,
            parallel_kind=self.parallel_kind,
        )

    @property
    def values(self):
        return self._values

    @property
    def data(self):
        return self._data

    @property
    def data_dump(self):
        return ujson.dumps(self._data)

    @property
    def config_dump(self):
        return self.config.to_light_dict(dump=True)

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
    def queue(self):
        return self.config.queue

    @property
    def nocache(self):
        return self.config.nocache
