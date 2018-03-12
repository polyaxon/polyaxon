# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from polyaxon_schemas.environments import HorovodClusterConfig
from polyaxon_schemas.polyaxonfile.specification.frameworks import HorovodSpecification
from polyaxon_schemas.utils import TaskType

from spawners.experiment_spawner import ExperimentSpawner

logger = logging.getLogger('polyaxon.spawners.horovod')


class HorovodSpawner(ExperimentSpawner):

    def create_workers(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)

        cluster, is_distributed, = self.spec.cluster_def
        resources = HorovodSpecification.get_worker_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return self._create_multi_pods(task_type=TaskType.WORKER,
                                       resources=resources,
                                       n_pods=n_pods)

    def delete_workers(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)
        self._delete_multi_pods(task_type=TaskType.WORKER, n_pods=n_pods)

    def start_experiment(self, user_token=None):
        experiment = super(HorovodSpawner, self).start_experiment(user_token=user_token)
        experiment[TaskType.WORKER] = self.create_workers()
        return experiment

    def stop_experiment(self):
        super(HorovodSpawner, self).stop_experiment()
        self.delete_workers()

    def get_cluster(self):
        cluster_def, is_distributed = self.spec.cluster_def

        job_name = self.pod_manager.get_job_name(task_type=TaskType.MASTER, task_idx=0)
        cluster_config = {
            TaskType.MASTER: [self._get_pod_address(job_name)]
        }

        workers = []
        for i in range(cluster_def.get(TaskType.WORKER, 0)):
            job_name = self.pod_manager.get_job_name(task_type=TaskType.WORKER, task_idx=i)
            workers.append(self._get_pod_address(job_name))

        cluster_config[TaskType.WORKER] = workers

        return HorovodClusterConfig.from_dict(cluster_config).to_dict()

