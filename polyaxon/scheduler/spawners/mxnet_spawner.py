import logging

from polyaxon_schemas.environments import MXNetClusterConfig
from polyaxon_schemas.polyaxonfile.specification.frameworks import MXNetSpecification
from polyaxon_schemas.utils import TaskType
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.templates.env_vars import get_env_var

logger = logging.getLogger('polyaxon.spawners.mxnet')


class MXNetSpawner(ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = False
    SERVER_SERVICE = False

    def get_env_vars(self, task_type, task_idx):
        role = TaskType.SCHEDULER if task_type == TaskType.MASTER else task_type
        env_vars = [
            get_env_var(name='DMLC_NUM_WORKER', value=self.get_n_pods(TaskType.WORKER)),
            get_env_var(name='DMLC_NUM_SERVER', value=self.get_n_pods(TaskType.SERVER)),
            get_env_var(name='DMLC_PS_ROOT_URI', value=self.pod_manager.get_job_name(
                task_type=TaskType.MASTER, task_idx=0)),
            get_env_var(name='DMLC_PS_ROOT_PORT', value=self.pod_manager.ports[0]),
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
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_resources = MXNetSpecification.get_ps_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_resources},
            TaskType.WORKER: worker_resources,
            TaskType.SERVER: ps_resources,
        }

    @property
    def node_selectors(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_node_selectors},
            TaskType.WORKER: worker_node_selectors,
            TaskType.SERVER: ps_node_selectors,
        }

    def get_resources(self, task_type, task_idx):
        return self.resources.get(task_type, {}).get(task_idx)

    def get_node_selectors(self, task_type, task_idx):
        return self.node_selectors.get(task_type, {}).get(task_idx)

    def get_n_pods(self, task_type):
        return self.spec.cluster_def[0].get(task_type, 0)

    def start_experiment(self, user_token=None):
        experiment = super(MXNetSpawner, self).start_experiment(user_token=user_token)
        experiment[TaskType.WORKER] = self.create_multi_jobs(task_type=TaskType.WORKER,
                                                             add_service=self.WORKER_SERVICE)
        experiment[TaskType.SERVER] = self.create_multi_jobs(task_type=TaskType.SERVER,
                                                             add_service=self.SERVER_SERVICE)
        return experiment

    def stop_experiment(self):
        super(MXNetSpawner, self).stop_experiment()
        self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE)
        self.delete_multi_jobs(task_type=TaskType.SERVER, has_service=self.SERVER_SERVICE)

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

        servers = []
        for i in range(cluster_def.get(TaskType.SERVER, 0)):
            job_name = self.pod_manager.get_job_name(task_type=TaskType.SERVER, task_idx=i)
            servers.append(self._get_pod_address(job_name))

        cluster_config[TaskType.SERVER] = servers

        return MXNetClusterConfig.from_dict(cluster_config).to_dict()
