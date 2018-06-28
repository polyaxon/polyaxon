from libs.paths.experiments import get_experiment_outputs_path
from polyaxon_schemas.environments import TensorflowClusterConfig
from polyaxon_schemas.polyaxonfile.specification.frameworks import TensorflowSpecification
from polyaxon_schemas.utils import TaskType
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.templates.env_vars import get_env_var


class TensorflowSpawner(ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = True
    PS_SERVICE = True

    def get_env_vars(self, task_type, task_idx):
        tf_config = {
            'cluster': self.get_cluster(),
            'task': {'type': task_type, 'index': task_idx},
            'model_dir': get_experiment_outputs_path(
                persistence_outputs=self.persistence_config.outputs,
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
            TaskType.MASTER: {0: self.spec.master_node_selectors},
            TaskType.WORKER: worker_node_selectors,
            TaskType.PS: ps_node_selectors,
        }

    def get_resources(self, task_type, task_idx):
        return self.resources.get(task_type, {}).get(task_idx)

    def get_node_selectors(self, task_type, task_idx):
        return self.node_selectors.get(task_type, {}).get(task_idx)

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
        super().stop_experiment()
        self.delete_multi_jobs(task_type=TaskType.WORKER, has_service=self.WORKER_SERVICE)
        self.delete_multi_jobs(task_type=TaskType.PS, has_service=self.PS_SERVICE)

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
        for i in range(cluster_def.get(TaskType.PS, 0)):
            job_name = self.pod_manager.get_job_name(task_type=TaskType.PS, task_idx=i)
            servers.append(self._get_pod_address(job_name))

        cluster_config[TaskType.PS] = servers

        return TensorflowClusterConfig.from_dict(cluster_config).to_dict()
