# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from polyaxon_schemas.environments import PytorchClusterConfig
from polyaxon_schemas.polyaxonfile.specification.frameworks import PytorchSpecification
from polyaxon_schemas.utils import TaskType

from spawners.experiment_spawner import ExperimentSpawner
from spawners.templates.config_maps import get_env_var

logger = logging.getLogger('polyaxon.spawners.pytorch')


class PytorchSpawner(ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = False

    def get_env_vars(self, task_type, task_idx):
        if task_type == TaskType.MASTER:
            rank = 0
            master_addr = 'localhost'
        else:
            rank = task_idx + 1
            master_addr = self.pod_manager.get_job_name(task_type=TaskType.MASTER, task_idx=0)
        env_vars = [
            get_env_var('MASTER_ADDR', master_addr),
            get_env_var('MASTER_PORT', self.pod_manager.ports[0]),
            get_env_var('WORLD_SIZE', self.get_n_pods(TaskType.WORKER) + 1),
            get_env_var(name='RANK', value=rank)
        ]
        return env_vars

    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_resources},
            TaskType.WORKER: worker_resources,
        }

    def get_resources(self, task_type, task_idx):
        return self.resources.get(task_type, {}).get(task_idx)

    def get_n_pods(self, task_type):
        return self.spec.cluster_def[0].get(task_type, 0)

    def start_experiment(self, user_token=None):
        experiment = super(PytorchSpawner, self).start_experiment(user_token=user_token)
        experiment[TaskType.WORKER] = self.create_multi_jobs(task_type=TaskType.WORKER,
                                                             add_service=self.WORKER_SERVICE)
        return experiment

    def stop_experiment(self):
        super(PytorchSpawner, self).stop_experiment()
        self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE)

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

        return PytorchClusterConfig.from_dict(cluster_config).to_dict()

