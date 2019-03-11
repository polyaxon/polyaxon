
from constants.experiment_jobs import get_experiment_job_uuid
from constants.k8s_jobs import EXPERIMENT_KF_JOB_NAME_FORMAT
from scheduler.spawners.kf_experiment_spawner import KFExperimentSpawner
from scheduler.spawners.templates import kubeflow
from scheduler.spawners.templates.kubeflow import KUBEFLOW_JOB_GROUP
from schemas.environments import MPIClusterConfig
from schemas.specifications import MPISpecification
from schemas.tasks import TaskType


class MPIJobSpawnerMixin(object):
    def create_job_uuids(self):
        job_uuids = {
            TaskType.WORKER:
                [get_experiment_job_uuid(self.experiment_uuid_instance, TaskType.WORKER, i)
                 for i in range(self.get_n_pods(task_type=TaskType.WORKER))]
        }
        return job_uuids

    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = MPISpecification.get_worker_resources(
            environment=self.spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.WORKER: worker_resources,
        }

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = MPISpecification.get_worker_node_selectors(
            environment=self.spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.WORKER: worker_node_selectors,
        }

    @property
    def affinities(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_affinities = MPISpecification.get_worker_affinities(
            environment=self.spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.WORKER: worker_affinities,
        }

    @property
    def tolerations(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_tolerations = MPISpecification.get_worker_tolerations(
            environment=self.spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
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

    def get_cluster(self):
        cluster_def, _ = self.spec.cluster_def
        cluster_config = {}

        workers = []
        for i in range(cluster_def.get(TaskType.WORKER, 0)):
            resource_name = self.resource_manager.get_resource_name(task_type=TaskType.WORKER,
                                                                    task_idx=i)
            workers.append(self._get_pod_address(resource_name))

        cluster_config[TaskType.WORKER] = workers

        return MPIClusterConfig.from_dict(cluster_config).to_dict()


class MPIJobSpawner(MPIJobSpawnerMixin, KFExperimentSpawner):
    KIND = kubeflow.PYTORCH_JOB_KIND
    VERSION = kubeflow.PYTORCH_JOB_VERSION
    PLURAL = kubeflow.PYTORCH_JOB_PLURAL

    def start_experiment(self):
        labels = self.resource_manager.experiment_labels
        template_spec = self.create_multi_jobs(task_type=TaskType.WORKER)
        resource_name = EXPERIMENT_KF_JOB_NAME_FORMAT.format(
            experiment_uuid=self.resource_manager.experiment_uuid)
        custom_object = self.resource_manager.get_custom_object(resource_name=resource_name,
                                                                kind=self.KIND,
                                                                api_version=self.api_version,
                                                                labels=labels,
                                                                template_spec=template_spec)
        self.create_or_update_custom_object(name=resource_name,
                                            group=KUBEFLOW_JOB_GROUP,
                                            version=self.VERSION,
                                            plural=self.PLURAL,
                                            data=custom_object)
        return custom_object
