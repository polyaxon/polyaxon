# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from polyaxon_schemas.environments import PodResourcesConfig
from polyaxon_schemas.polyaxonfile.specification.utils import (
    get_task_configs,
    get_task_job_resources
)
from polyaxon_schemas.utils import TaskType


class TensorflowSpecification(object):

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

    @staticmethod
    def get_worker_configs(environment, cluster, is_distributed):
        if environment is None or environment.tensorflow is None:
            return {}
        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=environment.tensorflow.worker_configs,
                                default_config=environment.tensorflow.default_worker_config,
                                task_type=TaskType.WORKER)

    @staticmethod
    def get_ps_configs(environment, cluster, is_distributed):
        if environment is None or environment.tensorflow is None:
            return {}
        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=environment.tensorflow.ps_configs,
                                default_config=environment.tensorflow.default_ps_config,
                                task_type=TaskType.PS)

    @staticmethod
    def get_worker_resources(environment, cluster, is_distributed):
        if environment is None or environment.tensorflow is None:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.tensorflow.worker_resources,
            default_resources=environment.tensorflow.default_worker_resources,
            task_type=TaskType.WORKER)

    @staticmethod
    def get_ps_resources(environment, cluster, is_distributed):
        if environment is None or environment.tensorflow is None:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.tensorflow.ps_resources,
            default_resources=environment.tensorflow.default_ps_resources,
            task_type=TaskType.PS)

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


class HorovodSpecification(object):

    @staticmethod
    def get_cluster_def(cluster, horovod_config):
        is_distributed = False
        if not horovod_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = horovod_config.n_workers
        if horovod_config.n_workers != 0:
            is_distributed = True

        return cluster, is_distributed

    @staticmethod
    def get_worker_configs(environment, cluster, is_distributed):
        if environment is None or environment.horovod is None:
            return {}
        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=environment.horovod.worker_configs,
                                default_config=environment.horovod.default_worker_config,
                                task_type=TaskType.WORKER)

    @staticmethod
    def get_worker_resources(environment, cluster, is_distributed):
        if environment is None or environment.horovod is None:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.horovod.worker_resources,
            default_resources=environment.horovod.default_worker_resources,
            task_type=TaskType.WORKER)

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


class PytorchSpecification(object):

    @staticmethod
    def get_cluster_def(cluster, pytorch_config):
        is_distributed = False
        if not pytorch_config:
            return cluster, is_distributed

        cluster[TaskType.WORKER] = pytorch_config.n_workers
        if pytorch_config.n_workers != 0:
            is_distributed = True

        return cluster, is_distributed

    @staticmethod
    def get_worker_configs(environment, cluster, is_distributed):
        if environment is None or environment.pytorch is None:
            return {}
        return get_task_configs(cluster=cluster,
                                is_distributed=is_distributed,
                                configs=environment.pytorch.worker_configs,
                                default_config=environment.pytorch.default_worker_config,
                                task_type=TaskType.WORKER)

    @staticmethod
    def get_worker_resources(environment, cluster, is_distributed):
        if environment is None or environment.pytorch is None:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.pytorch.worker_resources,
            default_resources=environment.pytorch.default_worker_resources,
            task_type=TaskType.WORKER)

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


class MXNetSpecification(object):

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

    @staticmethod
    def get_worker_resources(environment, cluster, is_distributed):
        if environment is None or environment.mxnet is None:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.mxnet.worker_resources,
            default_resources=environment.mxnet.default_worker_resources,
            task_type=TaskType.WORKER)

    @staticmethod
    def get_ps_resources(environment, cluster, is_distributed):
        if environment is None or environment.mxnet is None:
            return None
        return get_task_job_resources(
            cluster=cluster,
            is_distributed=is_distributed,
            resources=environment.mxnet.ps_resources,
            default_resources=environment.mxnet.default_ps_resources,
            task_type=TaskType.SERVER)

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
