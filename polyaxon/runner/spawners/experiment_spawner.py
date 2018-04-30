import logging

from polyaxon_k8s.manager import K8SManager
from polyaxon_schemas.utils import TaskType
from runner.spawners.base import get_pod_volumes
from runner.spawners.templates import config_maps, constants, pods, services

logger = logging.getLogger('polyaxon.spawners.experiment')


class ExperimentSpawner(K8SManager):
    MASTER_SERVICE = False

    def __init__(self,
                 project_name,
                 experiment_name,
                 project_uuid,
                 experiment_uuid,
                 spec,
                 experiment_group_uuid=None,
                 experiment_group_name=None,
                 original_name=None,
                 cloning_strategy=None,
                 k8s_config=None,
                 namespace='default',
                 in_cluster=False,
                 job_container_name=None,
                 job_docker_image=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 ports=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 sidecar_args_fn=None,
                 persist=False):
        self.spec = spec
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.original_name = original_name
        self.cloning_strategy = cloning_strategy
        self.pod_manager = pods.PodManager(namespace=namespace,
                                           project_name=self.project_name,
                                           experiment_group_name=self.experiment_group_name,
                                           experiment_name=self.experiment_name,
                                           project_uuid=self.project_uuid,
                                           experiment_group_uuid=self.experiment_group_uuid,
                                           experiment_uuid=experiment_uuid,
                                           job_container_name=job_container_name,
                                           job_docker_image=job_docker_image,
                                           sidecar_container_name=sidecar_container_name,
                                           sidecar_docker_image=sidecar_docker_image,
                                           role_label=role_label,
                                           type_label=type_label,
                                           ports=ports,
                                           use_sidecar=use_sidecar,
                                           sidecar_config=sidecar_config)
        self.sidecar_args_fn = sidecar_args_fn or constants.SIDECAR_ARGS_FN
        self.persist = persist

        super(ExperimentSpawner, self).__init__(k8s_config=k8s_config,
                                                namespace=namespace,
                                                in_cluster=in_cluster)

    def get_env_vars(self, task_type, task_idx):
        return None

    def get_resources(self, task_type, task_idx):
        return self.spec.master_resources

    def get_n_pods(self, task_type):
        return 0

    def _create_job(self,
                    task_type,
                    task_idx,
                    add_service,
                    command=None,
                    args=None,
                    sidecar_args_fn=None,
                    env_vars=None,
                    resources=None,
                    restart_policy='Never'):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        sidecar_args = sidecar_args_fn(pod_id=job_name)
        labels = self.pod_manager.get_labels(task_type=task_type, task_idx=task_idx)

        volumes, volume_mounts = get_pod_volumes()
        pod = self.pod_manager.get_pod(task_type=task_type,
                                       task_idx=task_idx,
                                       volume_mounts=volume_mounts,
                                       volumes=volumes,
                                       env_vars=env_vars,
                                       command=command,
                                       args=args,
                                       sidecar_args=sidecar_args,
                                       resources=resources,
                                       restart_policy=restart_policy)
        pod_resp, _ = self.create_or_update_pod(name=job_name, data=pod)

        service = services.get_service(namespace=self.namespace,
                                       name=job_name,
                                       labels=labels,
                                       ports=self.pod_manager.ports,
                                       target_ports=self.pod_manager.ports)

        results = {'pod': pod_resp.to_dict()}
        if add_service:
            service_resp, _ = self.create_or_update_service(name=job_name, data=service)
            results['service'] = service_resp.to_dict()
        return results

    def create_multi_jobs(self, task_type, add_service):
        resp = []
        n_pods = self.get_n_pods(task_type=task_type)
        for i in range(n_pods):
            command, args = self.get_pod_command_args(task_type=task_type, task_idx=i)
            env_vars = self.get_env_vars(task_type=task_type, task_idx=i)
            resources = self.get_resources(task_type=task_type, task_idx=i)
            resp.append(self._create_job(task_type=task_type,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         sidecar_args_fn=self.sidecar_args_fn,
                                         env_vars=env_vars,
                                         resources=resources,
                                         add_service=add_service))
        return resp

    def _delete_job(self, task_type, task_idx, has_service):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        self.delete_pod(name=job_name)
        if has_service:
            self.delete_service(name=job_name)

    def delete_multi_jobs(self, task_type, has_service):
        n_pods = self.get_n_pods(task_type=task_type)
        for i in range(n_pods):
            self._delete_job(task_type=task_type, task_idx=i, has_service=has_service)

    def get_pod_command_args(self, task_type, task_idx):
        if not self.spec.run_exec or not self.spec.run_exec.cmd:
            raise ValueError('The specification must contain a command.')

        cmd = self.spec.run_exec.cmd.split(' ')
        cmd = [c.strip().strip('\\') for c in cmd if (c and c != '\\')]
        cmd = [c for c in cmd if (c and c != '\\')]
        return cmd, []

    def create_master(self):
        command, args = self.get_pod_command_args(task_type=TaskType.MASTER, task_idx=0)
        env_vars = self.get_env_vars(task_type=TaskType.MASTER, task_idx=0)
        resources = self.get_resources(task_type=TaskType.MASTER, task_idx=0)
        return self._create_job(task_type=TaskType.MASTER,
                                task_idx=0,
                                command=command,
                                args=args,
                                sidecar_args_fn=self.sidecar_args_fn,
                                env_vars=env_vars,
                                resources=resources,
                                add_service=self.MASTER_SERVICE)

    def delete_master(self):
        self._delete_job(task_type=TaskType.MASTER, task_idx=0, has_service=self.MASTER_SERVICE)

    def create_experiment_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(experiment_uuid=self.experiment_uuid)
        config_map = config_maps.get_config_map(
            namespace=self.namespace,
            project_name=self.project_name,
            experiment_group_name=self.experiment_group_name,
            experiment_name=self.experiment_name,
            project_uuid=self.project_uuid,
            experiment_group_uuid=self.experiment_group_uuid,
            experiment_uuid=self.experiment_uuid,
            original_name=self.original_name,
            cloning_strategy=self.cloning_strategy,
            cluster_def=self.get_cluster(),
            declarations=self.spec.declarations,
            log_level=self.spec.log_level
        )

        self.create_or_update_config_map(name=name, body=config_map, reraise=True)

    def create_experiment_secret(self, user_token):
        name = constants.SECRET_NAME.format(experiment_uuid=self.experiment_uuid)
        secret = config_maps.get_secret(
            namespace=self.namespace,
            project_name=self.project_name,
            experiment_group_name=self.experiment_group_name,
            experiment_name=self.experiment_name,
            project_uuid=self.project_uuid,
            experiment_group_uuid=self.experiment_group_uuid,
            experiment_uuid=self.experiment_uuid,
            user_token=user_token
        )

        self.create_or_update_secret(name=name, body=secret, reraise=True)

    def delete_experiment_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(experiment_uuid=self.experiment_uuid)
        self.delete_config_map(name, reraise=True)

    def delete_experiment_secret(self):
        name = constants.SECRET_NAME.format(experiment_uuid=self.experiment_uuid)
        self.delete_secret(name, reraise=True)

    def start_experiment(self, user_token=None):
        self.create_experiment_config_map()
        self.create_experiment_secret(user_token)
        master_resp = self.create_master()
        return {
            TaskType.MASTER: master_resp,
        }

    def stop_experiment(self):
        self.delete_experiment_config_map()
        self.delete_experiment_secret()
        self.delete_master()

    def _get_pod_address(self, host):
        return '{}:{}'.format(host, self.pod_manager.ports[0])

    def get_cluster(self):
        job_name = self.pod_manager.get_job_name(task_type=TaskType.MASTER, task_idx=0)
        return {
            TaskType.MASTER: [self._get_pod_address(job_name)]
        }
