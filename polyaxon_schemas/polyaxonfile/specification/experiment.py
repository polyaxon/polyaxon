# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.specification.frameworks import (
    HorovodSpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from polyaxon_schemas.polyaxonfile.specification.job import JobSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import Frameworks, TaskType


class ExperimentSpecification(JobSpecification):
    """The Base polyaxonfile specification (parsing and validation of Polyaxonfiles/Configurations).

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        DECLARATIONS: variables/modules that can be reused.
        BUILD: defines the build step where the user can set a docker image definition
        RUN: defines the run step where the user can run a command
    """
    _SPEC_KIND = BaseSpecification._EXPERIMENT  # pylint:disable=protected-access

    POSSIBLE_SECTIONS = JobSpecification.POSSIBLE_SECTIONS + (
        JobSpecification.DECLARATIONS,
        JobSpecification.MODEL,
        JobSpecification.TRAIN,
        JobSpecification.EVAL
    )
    REQUIRED_SECTIONS = BaseSpecification.REQUIRED_SECTIONS

    @cached_property
    def is_runnable(self):
        """Checks of the sections required to run experiment exist."""
        sections = set(self.validated_data.keys())
        condition = (self.RUN in sections or
                     {self.MODEL, self.TRAIN} <= sections or
                     {self.MODEL, self.EVAL} <= sections)
        if condition:
            return True
        return False

    @cached_property
    def model(self):
        return self.validated_data.get(self.MODEL, None)

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
    def framework(self):
        if not self.environment:
            return None

        if self.environment.tensorflow:
            return Frameworks.TENSORFLOW

        if self.environment.horovod:
            return Frameworks.HOROVOD

        if self.environment.mxnet:
            return Frameworks.MXNET

        if self.environment.pytorch:
            return Frameworks.PYTORCH

    @cached_property
    def cluster_def(self):
        cluster = {
            TaskType.MASTER: 1,
        }
        is_distributed = False
        environment = self.environment

        if not environment:
            return cluster, is_distributed

        if environment.tensorflow:
            return TensorflowSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=environment.tensorflow)
        if environment.horovod:
            return HorovodSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=environment.horovod)
        if environment.mxnet:
            return MXNetSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=environment.mxnet)
        if environment.pytorch:
            return PytorchSpecification.get_cluster_def(
                cluster=cluster,
                framework_config=environment.pytorch)

        # No specified framework, It should return default standalone mode cluster definition
        return cluster, is_distributed

    @cached_property
    def total_resources(self):
        environment = self.environment

        if not environment:
            return None

        cluster, is_distributed = self.cluster_def

        # Check if any framework is defined
        if environment.tensorflow:
            return TensorflowSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=environment,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if environment.horovod:
            return HorovodSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=environment,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if environment.mxnet:
            return MXNetSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=environment,
                cluster=cluster,
                is_distributed=is_distributed
            )

        if environment.pytorch:
            return PytorchSpecification.get_total_resources(
                master_resources=self.master_resources,
                environment=environment,
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
