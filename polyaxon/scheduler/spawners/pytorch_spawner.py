import uuid

from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.templates.env_vars import get_env_var
from schemas.environments import PytorchClusterConfig
from schemas.specifications import PytorchSpecification
from schemas.tasks import TaskType


class PytorchSpawner(ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = False

    def create_job_uuids(self):
        job_uuids = super().create_job_uuids()
        job_uuids[TaskType.WORKER] = [
            uuid.uuid4().hex for _ in range(self.get_n_pods(task_type=TaskType.WORKER))]
        return job_uuids

    def get_env_vars(self, task_type, task_idx):
        if task_type == TaskType.MASTER:
            rank = 0
            master_addr = 'localhost'
        else:
            rank = task_idx + 1
            master_addr = self.resource_manager.get_resource_name(task_type=TaskType.MASTER,
                                                                  task_idx=0)
        env_vars = [
            get_env_var(name='MASTER_ADDR', value=master_addr),
            get_env_var(name='MASTER_PORT', value=self.ports[0]),
            get_env_var(name='WORLD_SIZE', value=self.get_n_pods(TaskType.WORKER) + 1),
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

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_node_selector},
            TaskType.WORKER: worker_node_selectors,
        }

    @property
    def affinities(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_affinities = PytorchSpecification.get_worker_affinities(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_affinity},
            TaskType.WORKER: worker_affinities,
        }

    @property
    def tolerations(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_tolerations = PytorchSpecification.get_worker_tolerations(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_tolerations},
            TaskType.WORKER: worker_tolerations,
        }

    def get_resources(self, task_type, task_idx):
        return self.resources.get(task_type, {}).get(task_idx)

    def get_node_selector(self, task_type, task_idx):
        return self.node_selectors.get(task_type, {}).get(task_idx)

    def get_affinity(self, task_type, task_idx):
        return self.affinities.get(task_type, {}).get(task_idx)

    def get_tolerations(self, task_type, task_idx):
        return self.tolerations.get(task_type, {}).get(task_idx)

    def get_n_pods(self, task_type):
        return self.spec.cluster_def[0].get(task_type, 0)

    def start_experiment(self):
        experiment = super().start_experiment()
        experiment[TaskType.WORKER] = self.create_multi_jobs(task_type=TaskType.WORKER,
                                                             add_service=self.WORKER_SERVICE)
        return experiment

    def stop_experiment(self):
        deleted = super().stop_experiment()
        if not self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE):
            deleted = False
        return deleted

    def get_cluster(self):
        cluster_def, _ = self.spec.cluster_def

        resource_name = self.resource_manager.get_resource_name(task_type=TaskType.MASTER,
                                                                task_idx=0)
        cluster_config = {
            TaskType.MASTER: [self._get_pod_address(resource_name)]
        }

        workers = []
        for i in range(cluster_def.get(TaskType.WORKER, 0)):
            resource_name = self.resource_manager.get_resource_name(task_type=TaskType.WORKER,
                                                                    task_idx=i)
            workers.append(self._get_pod_address(resource_name))

        cluster_config[TaskType.WORKER] = workers

        return PytorchClusterConfig.from_dict(cluster_config).to_dict()
