import logging

from polyaxon_schemas.environments import HorovodClusterConfig
from polyaxon_schemas.polyaxonfile.specification.frameworks import HorovodSpecification
from polyaxon_schemas.utils import TaskType
from scheduler.spawners.experiment_spawner import ExperimentSpawner

logger = logging.getLogger('polyaxon.spawners.horovod')


class HorovodSpawner(ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = True

    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = HorovodSpecification.get_worker_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_resources},
            TaskType.WORKER: worker_resources,
        }

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_node_selectors},
            TaskType.WORKER: worker_node_selectors,
        }

    def get_resources(self, task_type, task_idx):
        return self.resources.get(task_type, {}).get(task_idx)

    def get_node_selectors(self, task_type, task_idx):
        return self.node_selectors.get(task_type, {}).get(task_idx)

    def get_n_pods(self, task_type):
        return self.spec.cluster_def[0].get(task_type, 0)

    def start_experiment(self, user_token=None):
        experiment = super(HorovodSpawner, self).start_experiment(user_token=user_token)
        experiment[TaskType.WORKER] = self.create_multi_jobs(task_type=TaskType.WORKER,
                                                             add_service=self.WORKER_SERVICE)
        return experiment

    def stop_experiment(self):
        super(HorovodSpawner, self).stop_experiment()
        self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE)

    def get_cluster(self):
        cluster_def, _ = self.spec.cluster_def

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
