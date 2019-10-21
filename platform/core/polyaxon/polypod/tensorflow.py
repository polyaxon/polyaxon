import stores

from constants.experiment_jobs import get_experiment_job_uuid
from polypod.experiment import ExperimentSpawner
from polypod.templates.env_vars import get_env_var
from polypod.templates.labels import get_labels
from schemas import TaskType, TensorflowClusterConfig, TensorflowSpecification


class TensorflowSpawnerMixin(object):
    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = TensorflowSpecification.get_worker_resources(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_resources},
            TaskType.WORKER: worker_resources,
            TaskType.PS: ps_resources,
        }

    @property
    def labels(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_labels = TensorflowSpecification.get_worker_labels(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_labels = TensorflowSpecification.get_ps_labels(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_labels},
            TaskType.WORKER: worker_labels,
            TaskType.PS: ps_labels,
        }

    @property
    def annotations(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_annotations = TensorflowSpecification.get_worker_annotations(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_annotations = TensorflowSpecification.get_ps_annotations(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_annotations},
            TaskType.WORKER: worker_annotations,
            TaskType.PS: ps_annotations,
        }

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=self.spec.config.tensorflow,
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
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = TensorflowSpecification.get_ps_affinities(
            environment=self.spec.config.tensorflow,
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
            environment=self.spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_tolerations = TensorflowSpecification.get_ps_tolerations(
            environment=self.spec.config.tensorflow,
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
            get_experiment_job_uuid(self.experiment_uuid_instance, TaskType.WORKER, i)
            for i in range(self.get_n_pods(task_type=TaskType.WORKER))]
        job_uuids[TaskType.PS] = [
            get_experiment_job_uuid(self.experiment_uuid_instance, TaskType.PS, i)
            for i in range(self.get_n_pods(task_type=TaskType.PS))]
        return job_uuids

    def get_resources(self, task_type, task_idx):
        return self.resources.get(task_type, {}).get(task_idx)

    def get_annotations(self, task_type, task_idx):
        return self.annotations.get(task_type, {}).get(task_idx)

    def get_labels(self, task_type, task_idx, job_uuid):
        labels = self.resource_manager.get_labels(task_type=task_type,
                                                  task_idx=task_idx,
                                                  job_uuid=job_uuid)
        return get_labels(default_labels=labels,
                          labels=self.labels.get(task_type, {}).get(task_idx))

    def get_node_selector(self, task_type, task_idx):
        return self.node_selectors.get(task_type, {}).get(task_idx)

    def get_affinity(self, task_type, task_idx):
        return self.affinities.get(task_type, {}).get(task_idx)

    def get_tolerations(self, task_type, task_idx):
        return self.tolerations.get(task_type, {}).get(task_idx)

    def get_n_pods(self, task_type):
        return self.spec.cluster_def[0].get(task_type, 0)

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


class TensorflowSpawner(TensorflowSpawnerMixin, ExperimentSpawner):
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
