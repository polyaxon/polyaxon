# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import itertools
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
from polyaxon_schemas.settings import ClusterConfig, RunTypes, PodResourcesConfig
from polyaxon_schemas.utils import TaskType, to_list, SEARCH_METHODS


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


class Specification(BaseSpecification):
    """The Base polyaxonfile specification (parsing and validation of Polyaxonfiles/Configurations).

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        PROJECT: defines the project name this specification belongs to (must be unique).
        SETTINGS: defines the logging, run type and concurrent runs.
        ENVIRONMENT: defines the run environment for experiment.
        DECLARATIONS: variables/modules that can be reused.
        RUN_EXEC: defines the run step where the user can set a docker image to execute
        MODEL: defines the model to use based on the declarative API.
        TRAIN: defines how to train a model and how to read the data.
        EVAL: defines how to evaluate a modela how to read the data
    """

    def __init__(self, experiment, values):
        self._experiment = experiment
        super(Specification, self).__init__(values=values)
        if self.MATRIX in self.headers:
            raise PolyaxonConfigurationError(
                'Specification cannot contain a `matrix` section, you should '
                'use a GroupSpecification instead.')

    @classmethod
    def read(cls, values, experiment=None):
        if isinstance(values, cls):
            return values
        return cls(experiment=experiment, values=values)

    @property
    def experiment(self):
        return self._experiment

    @cached_property
    def experiment_path(self):
        return os.path.join(self.project_path, '{}'.format(self.experiment))

    @cached_property
    def parsed_data(self):
        return self._parsed_data

    @cached_property
    def validated_data(self):
        return self._validated_data

    @cached_property
    def is_runnable(self):
        """Checks of the sections required to run experiment exist."""
        sections = set(self.validated_data.keys())
        if (self.RUN_EXEC in sections or
                    {self.MODEL, self.TRAIN} <= sections or
                    {self.MODEL, self.EVAL} <= sections):
            return True
        return False

    @cached_property
    def run_exec(self):
        return self.validated_data.get(self.RUN_EXEC, None)

    @cached_property
    def model(self):
        return self.validated_data.get(self.MODEL, None)

    @cached_property
    def environment(self):
        return self.validated_data.get(self.ENVIRONMENT, None)

    @cached_property
    def train(self):
        return self.validated_data.get(self.TRAIN, None)

    @cached_property
    def eval(self):
        return self.validated_data.get(self.EVAL, None)

    @cached_property
    def declarations(self):
        return self.parsed_data.get(self.DECLARATIONS, None)

    @cached_property
    def cluster_def(self):
        cluster = {
            TaskType.MASTER: 1,
        }
        is_distributed = False
        environment = self.environment

        if environment:
            cluster[TaskType.WORKER] = environment.n_workers
            cluster[TaskType.PS] = environment.n_ps
            if environment.n_workers != 0 or environment.n_ps != 0:
                is_distributed = True

        return cluster, is_distributed

    def _get_configs(self, configs, default_config, task_type):
        cluster_def, is_distributed = self.cluster_def

        result_configs = {}
        if not is_distributed:
            return result_configs

        for session_config in configs or []:
            result_configs[session_config.index] = session_config

        if default_config:
            for i in range(cluster_def.get(task_type, 0)):
                result_configs[i] = result_configs.get(i, default_config)

        return result_configs

    @cached_property
    def worker_configs(self):
        environment = self.environment
        if environment is None:
            return {}
        return self._get_configs(configs=environment.worker_configs,
                                 default_config=environment.default_worker_config,
                                 task_type=TaskType.WORKER)

    @cached_property
    def ps_configs(self):
        environment = self.environment
        if environment is None:
            return {}
        return self._get_configs(configs=environment.ps_configs,
                                 default_config=environment.default_ps_config,
                                 task_type=TaskType.PS)

    def _get_job_resources(self, resources, default_resources, task_type):
        cluster_def, is_distributed = self.cluster_def

        if not is_distributed:
            return None

        result_resources = {}
        for resources_config in resources or []:
            result_resources[resources_config.index] = resources_config

        if default_resources:
            for i in range(cluster_def.get(task_type, 0)):
                result_resources[i] = result_resources.get(i, default_resources)

        return result_resources

    @cached_property
    def total_resources(self):
        master_resources = self.master_resources
        worker_resources = self.worker_resources
        ps_resources = self.ps_resources
        if not any([master_resources, worker_resources, ps_resources]):
            return None

        total_resources = PodResourcesConfig()

        if master_resources:
            total_resources += master_resources

        for w_resources in six.itervalues(worker_resources or {}):
            total_resources += w_resources

        for p_resources in six.itervalues(ps_resources or {}):
            total_resources += p_resources

        return total_resources.to_dict()

    @cached_property
    def master_resources(self):
        return self.environment.resources if self.environment else None

    @cached_property
    def worker_resources(self):
        environment = self.environment
        if environment is None:
            return None
        return self._get_job_resources(resources=environment.worker_resources,
                                       default_resources=environment.default_worker_resources,
                                       task_type=TaskType.WORKER)

    @cached_property
    def ps_resources(self):
        environment = self.environment
        if environment is None:
            return None
        return self._get_job_resources(resources=environment.ps_resources,
                                       default_resources=environment.default_ps_resources,
                                       task_type=TaskType.PS)

    def get_local_cluster(self,
                          host='127.0.0.1',
                          master_port=10000,
                          worker_port=11000,
                          ps_port=12000):
        def get_address(port):
            return '{}:{}'.format(host, port)

        cluster_def, is_distributed = self.cluster_def

        cluster_config = {
            TaskType.MASTER: [get_address(master_port)]
        }

        workers = []
        for i in range(cluster_def.get(TaskType.WORKER, 0)):
            workers.append(get_address(worker_port))
            worker_port += 1

        cluster_config[TaskType.WORKER] = workers

        ps = []
        for i in range(cluster_def.get(TaskType.PS, 0)):
            ps.append(get_address(ps_port))
            ps_port += 1

        cluster_config[TaskType.PS] = ps

        return ClusterConfig.from_dict(cluster_config)

    def get_cluster(self, **kwargs):
        if self.is_local:
            return self.get_local_cluster(**kwargs)


class GroupSpecification(BaseSpecification):
    """Parses Polyaxonfiles/Configuration, with matrix section definition.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        PROJECT: defines the project name this specification belongs to (must be unique).
        SETTINGS: defines the logging, run type and concurrent runs.
        ENVIRONMENT: defines the run environment for experiment.
        MATRIX: hyper parameters matrix definition.
        DECLARATIONS: variables/modules that can be reused.
        RUN_EXEC: defines the run step where the user can set a docker image to execute
        MODEL: defines the model to use based on the declarative API.
        TRAIN: defines how to train a model and how to read the data.
        EVAL: defines how to evaluate a model and how to read the data.
    """

    def __init__(self, values):
        self._values = to_list(values)

        self._data = reader.read(self._values)
        Parser.check_data(spec=self, data=self._data)
        headers = Parser.get_headers(spec=self, data=self._data)
        matrix = Parser.get_matrix(spec=self, data=self._data)
        try:
            self._matrix = validator.validate_matrix(matrix)
        except ValidationError as e:
            raise PolyaxonConfigurationError(e)
        try:
            self._headers = validator.validate_headers(spec=self, data=headers)
        except ValidationError as e:
            raise PolyaxonConfigurationError(e)
        self._parsed_data = []
        self._validated_data = []
        self._experiment_specs = []

        matrix_declarations = self.matrix_declarations if self.matrix_declarations else [{}]
        for i, matrix_declaration in enumerate(matrix_declarations):
            parsed_data = Parser.parse(self, self._data, matrix_declaration)
            self._validated_data.append(validator.validate(spec=self, data=parsed_data))
            self._parsed_data.append(parsed_data)
            self._experiment_specs.append(Specification(experiment=i, values=parsed_data))

    @cached_property
    def experiment_specs(self):
        return self._experiment_specs

    @cached_property
    def matrix(self):
        return self._matrix

    @cached_property
    def matrix_space(self):
        if not self.matrix:
            return 1

        space_size = 1
        for value in six.itervalues(self.matrix):
            space_size *= len(value.to_numpy())
        return space_size

    @cached_property
    def experiments_def(self):
        if self.settings:
            concurrent_experiments = self.settings.concurrent_experiments
            search_method = self.settings.search_method
        else:
            concurrent_experiments = 1
            search_method = SEARCH_METHODS.SEQUENTIAL
        return self.matrix_space, concurrent_experiments, search_method

    @cached_property
    def matrix_declarations(self):
        if not self.matrix:
            return []

        declarations = []
        keys = list(six.iterkeys(self.matrix))
        values = [v.to_numpy() for v in six.itervalues(self.matrix)]
        for v in itertools.product(*values):
            declarations.append(dict(zip(keys, v)))

        if len(declarations) != self.matrix_space:
            raise PolyaxonConfigurationError('The matrix declaration is not valid.')
        return declarations

    def get_declarations_at(self, experiment):
        if experiment > self.matrix_space:
            raise ValueError("""Could not find an experiment at index {},
               this file has {} experiments""".format(experiment, self.matrix_space))
        return self.matrix_declarations[experiment]

    def experiment_spec_at(self, experiment):
        if experiment > self.matrix_space:
            raise ValueError("""Could not find an experiment at index {},
               this file has {} experiments""".format(experiment, self.matrix_space))
        return self.experiment_specs[experiment]


class PluginSpecification(BaseSpecification):
    """The polyaxonfile specification for plugins.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        PROJECT: defines the project name this specification belongs to (must be unique).
        ENVIRONMENT: defines the run environment for experiment.
        RUN_EXEC: defines the run step where the user can set a docker image to execute
    """
    def __init__(self, values):
        super(PluginSpecification, self).__init__(values=values)
        if (self.RUN_EXEC not in self.validated_data or
                not self.validated_data[self.RUN_EXEC] or
                self.validated_data[self.RUN_EXEC].cmd is not None):
            raise PolyaxonConfigurationError(
                'Plugin specification must contain a valid `run` section.')

    @classmethod
    def read(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values=values)

    @cached_property
    def parsed_data(self):
        return self._parsed_data

    @cached_property
    def validated_data(self):
        return self._validated_data

    @cached_property
    def run_exec(self):
        return self.validated_data[self.RUN_EXEC]

    @cached_property
    def environment(self):
        return self.validated_data.get(self.ENVIRONMENT, None)

    @cached_property
    def resources(self):
        return self.environment.resources if self.environment else None
