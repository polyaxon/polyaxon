from constants.experiment_jobs import get_experiment_job_uuid
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.pod_cmd import get_horovod_pod_command_args
from schemas.environments import HorovodClusterConfig
from schemas.specifications import HorovodSpecification
from schemas.tasks import TaskType


class HorovodSpawnerMixin(object):
    def create_job_uuids(self):
        job_uuids = super().create_job_uuids()
        job_uuids[TaskType.WORKER] = [
            get_experiment_job_uuid(self.experiment_uuid_instance, TaskType.WORKER, i)
            for i in range(self.get_n_pods(task_type=TaskType.WORKER))]
        return job_uuids

    @property
    def resources(self):
        cluster, is_distributed, = self.spec.cluster_def
        worker_resources = HorovodSpecification.get_worker_resources(
            environment=self.spec.config.horovod,
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
            environment=self.spec.config.horovod,
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
        worker_affinities = HorovodSpecification.get_worker_affinities(
            environment=self.spec.config.horovod,
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
        worker_tolerations = HorovodSpecification.get_worker_tolerations(
            environment=self.spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return {
            TaskType.MASTER: {0: self.spec.master_affinity},
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

        return HorovodClusterConfig.from_dict(cluster_config).to_dict()


class HorovodSpawner(HorovodSpawnerMixin, ExperimentSpawner):
    MASTER_SERVICE = True
    WORKER_SERVICE = True

    def get_ports(self, ports):
        return ports or [constants.DEFAULT_SSH_PORT]

    def get_hosts(self, n_processes):
        worker_hosts = [
            '{}:{}'.format(
                self.resource_manager.get_resource_name(task_type=TaskType.WORKER, task_idx=i),
                n_processes)
            for i in range(self.get_n_pods(TaskType.WORKER))]
        return ','.join(['localhost:{}'.format(n_processes)] + worker_hosts)

    def get_master_command_args(self, task_type, task_idx):
        resources = self.get_resources(task_type=task_type, task_idx=task_idx)
        gpus = resources.gpu.requests
        n_processes = int(gpus) or 1
        n_workers = self.get_n_pods(TaskType.WORKER) + 1
        hosts = self.get_hosts(n_processes=n_processes)
        return get_horovod_pod_command_args(n_workers=n_workers,
                                            gpus=gpus,
                                            n_processes=n_processes,
                                            hosts=hosts,
                                            port=self.ports[0],
                                            run_config=self.spec.run)

    def get_worker_command_args(self):
        args = ["/usr/sbin/sshd -p {};sleep infinity".format(self.ports[0])]
        return ["/bin/bash", "-c"], args

    def get_pod_command_args(self, task_type, task_idx):
        if task_type == TaskType.MASTER:
            return self.get_master_command_args(task_type=task_type, task_idx=task_idx)
        return self.get_worker_command_args()

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
