import uuid

import stores

from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.templates.env_vars import get_env_var
from schemas.environments import TensorflowClusterConfig
from schemas.specifications import TensorflowSpecification
from schemas.tasks import TaskType


class TensorflowSpawner(ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = True
    PS_SERVICE = True

    def get_env_vars(self, task_type, task_idx):
        tf_config = {
            'cluster': self.get_cluster(),
            'task': {'type': task_type, 'index': task_idx},
            'model_dir': stores.get_experiment_outputs_path(
                persistence=self.persistence_config.outputs,
                experiment_name=self.experiment_name,
                cloning_strategy=self.cloning_strategy),
            'environment': 'cloud'
        }
        return get_env_var(name='TF_CONFIG', value=tf_config)

    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = TensorflowSpecification.get_worker_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_resources},
            TaskType.WORKER: worker_resources,
            TaskType.PS: ps_resources,
        }

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_node_selector},
            TaskType.WORKER: worker_node_selectors,
            TaskType.PS: ps_node_selectors,
        }

    @property
    def affinities(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_affinities = TensorflowSpecification.get_worker_affinities(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = TensorflowSpecification.get_ps_affinities(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_affinity},
            TaskType.WORKER: worker_affinities,
            TaskType.PS: ps_affinities,
        }

    @property
    def tolerations(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_tolerations = TensorflowSpecification.get_worker_tolerations(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_tolerations = TensorflowSpecification.get_ps_tolerations(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_tolerations},
            TaskType.WORKER: worker_tolerations,
            TaskType.PS: ps_tolerations,
        }

    def create_job_uuids(self):
        job_uuids = super().create_job_uuids()
        job_uuids[TaskType.WORKER] = [
            uuid.uuid4().hex for _ in range(self.get_n_pods(task_type=TaskType.WORKER))]
        job_uuids[TaskType.PS] = [
            uuid.uuid4().hex for _ in range(self.get_n_pods(task_type=TaskType.PS))]
        return job_uuids

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
        experiment[TaskType.PS] = self.create_multi_jobs(task_type=TaskType.PS,
                                                         add_service=self.PS_SERVICE)
        return experiment

    def stop_experiment(self):
        deleted = super().stop_experiment()
        if not self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE):
            deleted = False
        if not self.delete_multi_jobs(task_type=TaskType.PS, has_service=self.PS_SERVICE):
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

        servers = []
        for i in range(cluster_def.get(TaskType.PS, 0)):
            resource_name = self.resource_manager.get_resource_name(task_type=TaskType.PS,
                                                                    task_idx=i)
            servers.append(self._get_pod_address(resource_name))

        cluster_config[TaskType.PS] = servers

        return TensorflowClusterConfig.from_dict(cluster_config).to_dict()
