# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

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
from polyaxon_schemas.settings import ClusterConfig, RunTypes
from polyaxon_schemas.utils import TaskType, to_list


class Specification(object):
    """The polyaxonfile specification (parsing and validation of Polyaxonfiles/Configurations).

    HEADERS:
        version: the version of the file to be parsed and validated.
        matrix: hyper parameters matrix definition.
        declarations: variables/modules that can be reused.

    SECTIONS:

    """
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

        matrix_declarations = self.matrix_declarations if self.matrix_declarations else [{}]
        for matrix_declaration in matrix_declarations:
            parsed_data = Parser.parse(self, self._data, matrix_declaration)
            self._validated_data.append(validator.validate(spec=self, data=parsed_data))
            self._parsed_data.append(parsed_data)

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
        concurrent_experiments = self.settings.concurrent_experiments if self.settings else 1
        return self.matrix_space, concurrent_experiments

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
        return self.matrix_declarations[experiment]

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
        return self.settings.run_type if self.settings else RunTypes.LOCAL

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
        return self.get_project_path_at()

    def get_project_path_at(self, experiment=None):
        def get_path():
            project_path = None
            if self.settings:
                project_path = self.settings.logging.path

            if project_path:
                return project_path

            if self.run_type == RunTypes.LOCAL:
                return '/tmp/plx_logs/' + self.project.name

            return get_vol_path(self.project.name, constants.LOGS_VOLUME, self.run_type)

        path = get_path()
        if self.matrix_space == 1 or experiment is None:
            return path

        return os.path.join(path, experiment)

    @cached_property
    def parsed_data(self):
        if self.matrix_space == 1:
            return self.get_parsed_data_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
        please use `get_parsed_data_at(experiment)` instead.""".format(self.matrix_space))

    def get_parsed_data_at(self, experiment):
        if experiment > self.matrix_space:
            raise ValueError("""Could not find an experiment at index {},
            this file has {} experiments""".format(experiment, self.matrix_space))

        return self._parsed_data[experiment]

    @cached_property
    def validated_data(self):
        if self.matrix_space == 1:
            return self.get_validated_data_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
           please use `get_validated_data_at(experiment)` instead.""".format(self.matrix_space))

    def get_validated_data_at(self, experiment):
        if experiment > self.matrix_space:
            raise ValueError("""Could not find an experiment at index {},
               this file has {} experiments""".format(experiment, self.matrix_space))

        return self._validated_data[experiment]

    @cached_property
    def is_runnable(self):
        """Checks of the sections required to run experiment exist."""
        if self.matrix_space == 1:
            return self.is_runnable_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
        please use `is_runnable_at(experiment)` instead.""".format(self.matrix_space))

    def is_runnable_at(self, experiment):
        sections = set(self.get_validated_data_at(experiment).keys())
        if (self.RUN_EXEC in sections or
                {self.MODEL, self.TRAIN} <= sections or
                {self.MODEL, self.EVAL} <= sections):
            return True
        return False

    @cached_property
    def run_exec(self):
        if self.matrix_space == 1:
            return self.get_run_exec_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
            please use `get_run_at(experiment)` instead.""".format(self.matrix_space))

    def get_run_exec_at(self, experiment):
        return self.get_validated_data_at(experiment).get(self.RUN_EXEC, None)

    @cached_property
    def model(self):
        if self.matrix_space == 1:
            return self.get_model_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
        please use `get_model_at(experiment)` instead.""".format(self.matrix_space))

    def get_model_at(self, experiment):
        return self.get_validated_data_at(experiment).get(self.MODEL, None)

    @cached_property
    def environment(self):
        if self.matrix_space == 1:
            return self.get_environment_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
        please use `get_environment_at(experiment)` instead.""".format(self.matrix_space))

    def get_environment_at(self, experiment):
        return self.get_validated_data_at(experiment).get(self.ENVIRONMENT, None)

    @cached_property
    def train(self):
        if self.matrix_space == 1:
            return self.get_train_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
                please use `get_train_at(experiment)` instead.""".format(self.matrix_space))

    def get_train_at(self, experiment):
        return self.get_validated_data_at(experiment).get(self.TRAIN, None)

    @cached_property
    def eval(self):
        if self.matrix_space == 1:
            return self.get_eval_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
        please use `get_eval_at(experiment)` instead.""".format(self.matrix_space))

    def get_eval_at(self, experiment):
        return self.get_validated_data_at(experiment).get(self.EVAL, None)

    def _get_configs_at(self, experiment, configs, default_config, task_type):
        cluster_def, is_distributed = self.get_cluster_def_at(experiment)

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
        if self.matrix_space == 1:
            return self.get_worker_configs_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
           please use `get_worker_configs_at(experiment)` instead.""".format(self.matrix_space))

    def get_worker_configs_at(self, experiment):
        environment = self.get_environment_at(experiment)
        return self._get_configs_at(experiment,
                                    environment.worker_configs,
                                    environment.default_worker_config,
                                    TaskType.WORKER)

    @cached_property
    def ps_configs(self):
        if self.matrix_space == 1:
            return self.get_ps_configs_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
               please use `get_ps_configs_at(experiment)` instead.""".format(self.matrix_space))

    def get_ps_configs_at(self, experiment):
        environment = self.get_environment_at(experiment)
        return self._get_configs_at(experiment,
                                    environment.ps_configs,
                                    environment.default_ps_config,
                                    TaskType.PS)

    def _get_resource_at(self, experiment, resources, default_resources, task_type):
        cluster_def, is_distributed = self.get_cluster_def_at(experiment)

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
    def worker_resources(self):
        if self.matrix_space == 1:
            return self.get_worker_resource_at(0)
        raise AttributeError(
            "Current polyaxonfile has multiple experiments ({}),"
            "please use `get_worker_resource_at(experiment)` instead.".format(self.matrix_space))

    def get_worker_resource_at(self, experiment):
        environment = self.get_environment_at(experiment)
        return self._get_resource_at(experiment,
                                     environment.worker_resources,
                                     environment.default_worker_resources,
                                     TaskType.WORKER)

    @cached_property
    def ps_resources(self):
        if self.matrix_space == 1:
            return self.get_ps_resource_at(0)
        raise AttributeError(
            "Current polyaxonfile has multiple experiments ({}),"
            "please use `get_ps_resource_at(experiment)` instead.".format(self.matrix_space))

    def get_ps_resource_at(self, experiment):
        environment = self.get_environment_at(experiment)
        return self._get_resource_at(experiment,
                                     environment.ps_resources,
                                     environment.default_ps_resources,
                                     TaskType.PS)

    @cached_property
    def cluster_def(self):
        if self.matrix_space == 1:
            return self.get_cluster_def_at(0)
        raise AttributeError("""Current polyaxonfile has multiple experiments ({}),
        please use `get_train_at(experiment)` instead.""".format(self.matrix_space))

    def get_cluster_def_at(self, experiment):
        cluster = {
            TaskType.MASTER: 1,
        }
        is_distributed = False
        environment = self.get_environment_at(experiment)

        if environment:
            cluster[TaskType.WORKER] = environment.n_workers
            cluster[TaskType.PS] = environment.n_ps
            if environment.n_workers != 0 or environment.n_ps != 0:
                is_distributed = True

        return cluster, is_distributed

    def get_k8s_cluster(self, experiment=0, port=constants.DEFAULT_PORT):
        cluster_def, is_distributed = self.get_cluster_def_at(experiment)

        def get_address(host):
            return '{}:{}'.format(host, port)

        task_name = constants.TASK_NAME.format(project=self.project.name,
                                               experiment=experiment,
                                               task_type=TaskType.MASTER,
                                               task_id=0)
        cluster_config = {
            TaskType.MASTER: [get_address(task_name)]
        }

        workers = []
        for i in range(cluster_def.get(TaskType.WORKER, 0)):
            task_name = constants.TASK_NAME.format(
                project=self.project.name,
                experiment=experiment,
                task_type=TaskType.WORKER,
                task_id=i)
            workers.append(get_address(task_name))

        cluster_config[TaskType.WORKER] = workers

        ps = []
        for i in range(cluster_def.get(TaskType.PS, 0)):
            task_name = constants.TASK_NAME.format(
                project=self.project.name,
                experiment=experiment,
                task_type=TaskType.PS,
                task_id=i)
            ps.append(get_address(task_name))

        cluster_config[TaskType.PS] = ps

        return ClusterConfig.from_dict(cluster_config)

    def get_local_cluster(self, experiment=0,
                          host='127.0.0.1',
                          master_port=10000,
                          worker_port=11000,
                          ps_port=12000):
        def get_address(port):
            return '{}:{}'.format(host, port)

        cluster_def, is_distributed = self.get_cluster_def_at(experiment)

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

    def get_cluster(self, experiment=0):
        if self.is_local:
            return self.get_local_cluster(experiment)
        elif self.run_type in (RunTypes.MINIKUBE, RunTypes.KUBERNETES):
            return self.get_k8s_cluster(experiment)
