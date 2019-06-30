# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from hestia.cached_property import cached_property
from marshmallow import EXCLUDE

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.ops.experiment import ExperimentConfig
from polyaxon_schemas.ops.experiment.environment import ExperimentEnvironmentConfig
from polyaxon_schemas.ops.run import RunConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseRunSpecification
from polyaxon_schemas.specs.frameworks import (
    HorovodSpecification,
    MPISpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from polyaxon_schemas.utils import TaskType


class ExperimentSpecification(BaseRunSpecification):
    """The Base polyaxonfile specification (parsing and validation of Polyaxonfiles/Configurations).

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        PARAMS: variables/modules that can be reused.
        BUILD: defines the build step where the user can set a docker image definition
        RUN: defines the run step where the user can run a command
    """
    _SPEC_KIND = kinds.EXPERIMENT  # pylint:disable=protected-access

    SECTIONS = BaseRunSpecification.SECTIONS

    HEADER_SECTIONS = BaseRunSpecification.HEADER_SECTIONS + (
        BaseRunSpecification.FRAMEWORK,
    )

    POSSIBLE_SECTIONS = BaseRunSpecification.POSSIBLE_SECTIONS + (
        BaseRunSpecification.FRAMEWORK,
        BaseRunSpecification.DECLARATIONS,
        BaseRunSpecification.PARAMS,
        BaseRunSpecification.RUN,
    )

    ENVIRONMENT_CONFIG = ExperimentEnvironmentConfig
    CONFIG = ExperimentConfig

    @cached_property
    def params(self):
        return self.parsed_data.get(self.PARAMS, None)

    @cached_property
    def backend(self):
        return self.config.backend

    @cached_property
    def framework(self):
        return self.config.framework

    @cached_property
    def run(self):
        return self.config.run

    @cached_property
    def cluster_def(self):
        cluster = {
            TaskType.MASTER: 1,
        }
        is_distributed = False
        environment = self.environment

        if not environment:
            return cluster, is_distributed

        if self.config.tensorflow:
            return TensorflowSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=self.config.tensorflow)
        if self.config.horovod:
            return HorovodSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=self.config.horovod)
        if self.config.mxnet:
            return MXNetSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=self.config.mxnet)
        if self.config.pytorch:
            return PytorchSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=self.config.pytorch)
        if self.config.mpi:
            return MPISpecification.get_cluster_def(
                cluster={},
                framework_config=self.config.mpi)

        # No specified framework, It should return default standalone mode cluster definition
        return cluster, is_distributed

    @cached_property
    def total_resources(self):
        environment = self.environment

        if not environment:
            return None

        cluster, is_distributed = self.cluster_def

        # Check if any framework is defined
        if self.config.tensorflow:
            return TensorflowSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=self.config.tensorflow,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if self.config.horovod:
            return HorovodSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=self.config.horovod,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if self.config.mxnet:
            return MXNetSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=self.config.mxnet,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if self.config.pytorch:
            return PytorchSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=self.config.pytorch,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if self.config.mpi:
            return MPISpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=self.config.mpi,
                cluster=cluster,
                is_distributed=is_distributed
            )

        # default value is the master resources
        return self.master_resources

    @cached_property
    def master_resources(self):
        return self.environment.resources if self.environment else None

    @cached_property
    def master_node_selector(self):
        return self.environment.node_selector if self.environment else None

    @cached_property
    def master_affinity(self):
        return self.environment.affinity if self.environment else None

    @cached_property
    def master_tolerations(self):
        return self.environment.tolerations if self.environment else None

    @classmethod
    def create_specification(cls,  # pylint:disable=arguments-differ
                             build_config,
                             run_config,
                             to_dict=True):
        try:
            specification = BaseRunSpecification.create_specification(
                build_config=build_config, to_dict=True)
        except PolyaxonConfigurationError:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        if isinstance(run_config, RunConfig):
            r_config = run_config.to_light_dict()
        elif isinstance(run_config, Mapping):
            r_config = RunConfig.from_dict(run_config, unknown=EXCLUDE)
            r_config = r_config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of RunConfig.')

        specification[cls.KIND] = cls._SPEC_KIND
        specification[cls.RUN] = r_config

        if to_dict:
            return specification
        return cls.read(specification)
