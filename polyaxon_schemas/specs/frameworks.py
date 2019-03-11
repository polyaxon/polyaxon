# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from polyaxon_schemas.ops.environments.resources import PodResourcesConfig
from polyaxon_schemas.specs.utils import (
    get_task_configs,
    get_task_job_affinities,
    get_task_job_node_selectors,
    get_task_job_resources,
    get_task_job_tolerations
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
        return None

    @staticmethod
    def get_cluster_def(cluster, framework_config):
        pass

    @classmethod
    def get_worker_configs(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=environment.worker_configs,
                                default_config=environment.default_worker_config,
                                task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_configs(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=environment.ps_configs,
                                default_config=environment.default_ps_config,
                                task_type=cls.TASK_PS)

    @classmethod
    def get_worker_resources(cls, environment, cluster, is_distributed):
        if not environment:
            return None

        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.worker_resources,
            default_resources=environment.default_worker_resources,
            task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_resources(cls, environment, cluster, is_distributed):
        if not environment:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.ps_resources,
            default_resources=environment.default_ps_resources,
            task_type=cls.TASK_PS)

    @classmethod
    def get_total_resources(cls, master_resources, environment, cluster, is_distributed):
        pass

    @classmethod
    def get_worker_node_selectors(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_job_node_selectors(
            cluster=cluster,
            is_distributed=is_distributed,
            node_selectors=environment.worker_node_selectors,
            default_node_selector=environment.default_worker_node_selector,
            task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_node_selectors(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_job_node_selectors(
            cluster=cluster,
            is_distributed=is_distributed,
            node_selectors=environment.ps_node_selectors,
            default_node_selector=environment.default_ps_node_selector,
            task_type=cls.TASK_PS)

    @classmethod
    def get_worker_tolerations(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_job_tolerations(
            cluster=cluster,
            is_distributed=is_distributed,
            tolerations=environment.worker_tolerations,
            default_tolerations=environment.default_worker_tolerations,
            task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_tolerations(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_job_tolerations(
            cluster=cluster,
            is_distributed=is_distributed,
            tolerations=environment.ps_tolerations,
            default_tolerations=environment.default_ps_tolerations,
            task_type=cls.TASK_PS)

    @classmethod
    def get_worker_affinities(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_job_affinities(
            cluster=cluster,
            is_distributed=is_distributed,
            affinities=environment.worker_affinities,
            default_affinity=environment.default_worker_affinity,
            task_type=cls.TASK_WORKER)

    @classmethod
    def get_ps_affinities(cls, environment, cluster, is_distributed):
        if not environment:
            return {}

        return get_task_job_affinities(
            cluster=cluster,
            is_distributed=is_distributed,
            affinities=environment.ps_affinities,
            default_affinity=environment.default_ps_affinity,
            task_type=cls.TASK_PS)


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
    def get_cluster_def(cluster, framework_config):
        is_distributed = False
        if not framework_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = framework_config.n_workers
        cluster[TaskType.PS] = framework_config.n_ps
        if framework_config.n_workers != 0 or framework_config.n_ps != 0:
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
    def get_cluster_def(cluster, framework_config):
        is_distributed = False
        if not framework_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = framework_config.n_workers
        if framework_config.n_workers != 0:
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
    def get_cluster_def(cluster, framework_config):
        is_distributed = False
        if not framework_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = framework_config.n_workers
        if framework_config.n_workers != 0:
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
    def get_cluster_def(cluster, framework_config):
        is_distributed = False
        if not framework_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = framework_config.n_workers
        cluster[TaskType.SERVER] = framework_config.n_ps
        if framework_config.n_workers != 0 or framework_config.n_ps != 0:
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


class MPISpecification(DistributedSpecificationInterface):
    @staticmethod
    def has_framework_environment(environment):
        return environment is not None and environment.mpi is not None

    @classmethod
    def get_framework_environment(cls, environment):
        if not cls.has_framework_environment(environment=environment):
            return None
        return environment.mpi

    @staticmethod
    def get_cluster_def(cluster, framework_config):
        is_distributed = False
        if not framework_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = framework_config.n_workers
        if framework_config.n_workers != 0:
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
