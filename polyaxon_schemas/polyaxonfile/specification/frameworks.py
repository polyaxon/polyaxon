# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from polyaxon_schemas.environments import PodResourcesConfig
from polyaxon_schemas.polyaxonfile.specification.utils import (
    get_task_configs,
    get_task_job_resources
)
from polyaxon_schemas.utils import TaskType


class DistributedSpecificationInterface(object):
    TASK_WORKER = TaskType.WORKER
    TASK_PS = TaskType.PS

    @staticmethod
    def has_framework_environment(environment):
        return False

    @staticmethod
    def get_framework_environment(environment):
        pass

    @staticmethod
    def get_cluster_def(cluster, tensorflow_config):
        pass

    @classmethod
    def get_worker_configs(cls, environment, cluster, is_distributed):
        framework_environment = cls.get_framework_environment(environment=environment)
        if not framework_environment:
            return {}

        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=framework_environment.worker_configs,
                                default_config=framework_environment.default_worker_config,
                                task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_configs(cls, environment, cluster, is_distributed):
        framework_environment = cls.get_framework_environment(environment=environment)
        if not framework_environment:
            return {}

        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=framework_environment.ps_configs,
                                default_config=framework_environment.default_ps_config,
                                task_type=cls.TASK_PS)

    @classmethod
    def get_worker_resources(cls, environment, cluster, is_distributed):
        framework_environment = cls.get_framework_environment(environment=environment)
        if not framework_environment:
            return None

        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=framework_environment.worker_resources,
            default_resources=framework_environment.default_worker_resources,
            task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_resources(cls, environment, cluster, is_distributed):
        framework_environment = cls.get_framework_environment(environment=environment)
        if not framework_environment:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=framework_environment.ps_resources,
            default_resources=framework_environment.default_ps_resources,
            task_type=cls.TASK_PS)

    @classmethod
    def get_total_resources(cls, master_resources, environment, cluster, is_distributed):
        pass

    @staticmethod
    def get_worker_node_selectors(environment, cluster, is_distributed):
        pass

    @staticmethod
    def get_ps_node_selectors(environment, cluster, is_distributed):
        pass


class TensorflowSpecification(DistributedSpecificationInterface):
    @staticmethod
    def has_framework_environment(environment):
        return environment is not None and environment.tensorflow is not None

    @classmethod
    def get_framework_environment(cls, environment):
        if not cls.has_framework_environment(environment=environment):
            return None
        return environment.tensorflow

    @staticmethod
    def get_cluster_def(cluster, tensorflow_config):
        is_distributed = False
        if not tensorflow_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = tensorflow_config.n_workers
        cluster[TaskType.PS] = tensorflow_config.n_ps
        if tensorflow_config.n_workers != 0 or tensorflow_config.n_ps != 0:
            is_distributed = True

        return cluster, is_distributed

    @classmethod
    def get_total_resources(cls, master_resources, environment, cluster, is_distributed):
        worker_resources = cls.get_worker_resources(
            environment=environment,
            cluster=cluster,
            is_distributed=is_distributed,
        )
        ps_resources = cls.get_ps_resources(
            environment=environment,
            cluster=cluster,
            is_distributed=is_distributed,
        )
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


class HorovodSpecification(DistributedSpecificationInterface):
    @staticmethod
    def has_framework_environment(environment):
        return environment is not None and environment.horovod is not None

    @classmethod
    def get_framework_environment(cls, environment):
        if not cls.has_framework_environment(environment=environment):
            return None
        return environment.horovod

    @staticmethod
    def get_cluster_def(cluster, horovod_config):
        is_distributed = False
        if not horovod_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = horovod_config.n_workers
        if horovod_config.n_workers != 0:
            is_distributed = True

        return cluster, is_distributed

    @classmethod
    def get_total_resources(cls, master_resources, environment, cluster, is_distributed):
        worker_resources = cls.get_worker_resources(
            environment=environment,
            cluster=cluster,
            is_distributed=is_distributed,
        )

        if not any([master_resources, worker_resources]):
            return None

        total_resources = PodResourcesConfig()

        if master_resources:
            total_resources += master_resources

        for w_resources in six.itervalues(worker_resources or {}):
            total_resources += w_resources

        return total_resources.to_dict()


class PytorchSpecification(DistributedSpecificationInterface):
    @staticmethod
    def has_framework_environment(environment):
        return environment is not None and environment.pytorch is not None

    @classmethod
    def get_framework_environment(cls, environment):
        if not cls.has_framework_environment(environment=environment):
            return None
        return environment.pytorch

    @staticmethod
    def get_cluster_def(cluster, pytorch_config):
        is_distributed = False
        if not pytorch_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = pytorch_config.n_workers
        if pytorch_config.n_workers != 0:
            is_distributed = True

        return cluster, is_distributed

    @classmethod
    def get_total_resources(cls, master_resources, environment, cluster, is_distributed):
        worker_resources = cls.get_worker_resources(
            environment=environment,
            cluster=cluster,
            is_distributed=is_distributed,
        )

        if not any([master_resources, worker_resources]):
            return None

        total_resources = PodResourcesConfig()

        if master_resources:
            total_resources += master_resources

        for w_resources in six.itervalues(worker_resources or {}):
            total_resources += w_resources

        return total_resources.to_dict()


class MXNetSpecification(DistributedSpecificationInterface):
    TASK_PS = TaskType.SERVER

    @staticmethod
    def has_framework_environment(environment):
        return environment is not None and environment.mxnet is not None

    @classmethod
    def get_framework_environment(cls, environment):
        if not cls.has_framework_environment(environment=environment):
            return None
        return environment.mxnet

    @staticmethod
    def get_cluster_def(cluster, mxnet_config):
        is_distributed = False
        if not mxnet_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = mxnet_config.n_workers
        cluster[TaskType.SERVER] = mxnet_config.n_ps
        if mxnet_config.n_workers != 0 or mxnet_config.n_ps != 0:
            is_distributed = True

        return cluster, is_distributed

    @classmethod
    def get_total_resources(cls, master_resources, environment, cluster, is_distributed):
        worker_resources = cls.get_worker_resources(
            environment=environment,
            cluster=cluster,
            is_distributed=is_distributed,
        )
        ps_resources = cls.get_ps_resources(
            environment=environment,
            cluster=cluster,
            is_distributed=is_distributed,
        )
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
