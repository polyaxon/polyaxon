from constants.experiment_jobs import get_experiment_job_uuid
from polypod.experiment import ExperimentSpawner
from polypod.templates.env_vars import get_env_var
from polypod.templates.labels import get_labels
from schemas import MXNetClusterConfig, MXNetSpecification, TaskType


class MXNetSpawnerMixin(object):
    def create_job_uuids(self):
        job_uuids = super().create_job_uuids()
        job_uuids[TaskType.WORKER] = [
            get_experiment_job_uuid(self.experiment_uuid_instance, TaskType.WORKER, i)
            for i in range(self.get_n_pods(task_type=TaskType.WORKER))]
        job_uuids[TaskType.SERVER] = [
            get_experiment_job_uuid(self.experiment_uuid_instance, TaskType.PS, i)
            for i in range(self.get_n_pods(task_type=TaskType.PS))]
        return job_uuids

    def get_env_vars(self, task_type, task_idx):
        role = TaskType.SCHEDULER if task_type == TaskType.MASTER else task_type
        env_vars = [
            get_env_var(name='DMLC_NUM_WORKER', value=self.get_n_pods(TaskType.WORKER)),
            get_env_var(name='DMLC_NUM_SERVER', value=self.get_n_pods(TaskType.SERVER)),
            get_env_var(name='DMLC_PS_ROOT_URI', value=self.resource_manager.get_resource_name(
                task_type=TaskType.MASTER, task_idx=0)),
            get_env_var(name='DMLC_PS_ROOT_PORT', value=self.ports[0]),
            get_env_var(name='DMLC_ROLE', value=role)
        ]
        if task_type == TaskType.SERVER:
            env_vars.append(get_env_var(name='DMLC_SERVER_ID', value=task_idx))
        elif task_type == TaskType.WORKER:
            env_vars.append(get_env_var(name='DMLC_SERVER_ID', value=0))
            env_vars.append(get_env_var(name='DMLC_WORKER_ID', value=task_idx))

        return env_vars

    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = MXNetSpecification.get_worker_resources(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_resources = MXNetSpecification.get_ps_resources(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_resources},
            TaskType.WORKER: worker_resources,
            TaskType.SERVER: ps_resources,
        }

    @property
    def labels(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_labels = MXNetSpecification.get_worker_labels(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_labels = MXNetSpecification.get_ps_labels(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_labels},
            TaskType.WORKER: worker_labels,
            TaskType.SERVER: ps_labels,
        }

    @property
    def annotations(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_annotations = MXNetSpecification.get_worker_annotations(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_annotations = MXNetSpecification.get_ps_annotations(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_annotations},
            TaskType.WORKER: worker_annotations,
            TaskType.SERVER: ps_annotations,
        }

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_node_selector},
            TaskType.WORKER: worker_node_selectors,
            TaskType.SERVER: ps_node_selectors,
        }

    @property
    def affinities(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_affinities = MXNetSpecification.get_worker_affinities(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = MXNetSpecification.get_ps_affinities(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_affinity},
            TaskType.WORKER: worker_affinities,
            TaskType.SERVER: ps_affinities,
        }

    @property
    def tolerations(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_tolerations = MXNetSpecification.get_worker_tolerations(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_tolerations = MXNetSpecification.get_ps_tolerations(
            environment=self.spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_tolerations},
            TaskType.WORKER: worker_tolerations,
            TaskType.SERVER: ps_tolerations,
        }

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
        for i in range(cluster_def.get(TaskType.SERVER, 0)):
            resource_name = self.resource_manager.get_resource_name(task_type=TaskType.SERVER,
                                                                    task_idx=i)
            servers.append(self._get_pod_address(resource_name))

        cluster_config[TaskType.SERVER] = servers

        return MXNetClusterConfig.from_dict(cluster_config).to_dict()


class MXNetSpawner(MXNetSpawnerMixin, ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = False
    SERVER_SERVICE = False

    def start_experiment(self):
        experiment = super().start_experiment()
        experiment[TaskType.WORKER] = self.create_multi_jobs(task_type=TaskType.WORKER,
                                                             add_service=self.WORKER_SERVICE)
        experiment[TaskType.SERVER] = self.create_multi_jobs(task_type=TaskType.SERVER,
                                                             add_service=self.SERVER_SERVICE)
        return experiment

    def stop_experiment(self):
        deleted = super().stop_experiment()
        if not self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE):
            deleted = False
        if not self.delete_multi_jobs(task_type=TaskType.SERVER, has_service=self.SERVER_SERVICE):
            deleted = False
        return deleted
