from polyaxon.utils import config
from polyaxon_k8s.manager import K8SManager

from scheduler.spawners.templates.base_pods import get_pod_command_args
from scheduler.spawners.templates.env_vars import get_env_var, get_service_env_vars
from scheduler.spawners.templates.jobs import pods
from scheduler.spawners.templates.volumes import get_pod_volumes


class JobSpawner(K8SManager):
    def __init__(self,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 spec,
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
                 persist=False):
        self.spec = spec
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.pod_manager = pods.PodManager(namespace=namespace,
                                           project_name=self.project_name,
                                           project_uuid=self.project_uuid,
                                           job_name=job_name,
                                           job_uuid=job_uuid,
                                           job_container_name=job_container_name,
                                           job_docker_image=job_docker_image,
                                           sidecar_container_name=sidecar_container_name,
                                           sidecar_docker_image=sidecar_docker_image,
                                           role_label=role_label,
                                           type_label=type_label,
                                           ports=ports,
                                           use_sidecar=use_sidecar,
                                           sidecar_config=sidecar_config,
                                           log_level=self.spec.log_level)
        self.persist = persist

        super(JobSpawner, self).__init__(k8s_config=k8s_config,
                                         namespace=namespace,
                                         in_cluster=in_cluster)

    def get_env_vars(self):
        env_vars = get_service_env_vars(namespace=self.namespace)
        for k, v in config.get_requested_params(to_str=True).items():
            env_vars.append(get_env_var(name=k, value=v))

        return env_vars

    def get_pod_command_args(self):
        return get_pod_command_args(run_config=self.spec.run)

    def start_job(self, resources=None, node_selectors=None):
        volumes, volume_mounts = get_pod_volumes()
        command, args = self.get_pod_command_args()
        env_vars = self.get_env_vars()
        pod_resp = self.pod_manager.get_pod(
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            resources=resources,
            node_selector=node_selectors,
            restart_policy='Never')

        return pod_resp.to_dict()

    def stop_dockerizer(self):
        self.delete_pod(name=self.pod_manager.pod_name)
