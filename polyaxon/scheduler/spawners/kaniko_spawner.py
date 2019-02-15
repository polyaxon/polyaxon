import conf

from scheduler.spawners.dockerizer_spawner import DockerizerSpawner
from scheduler.spawners.templates import constants


class KanikoSpawner(DockerizerSpawner):
    def __init__(self,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 spec,
                 commit=None,
                 from_image=None,
                 dockerfile_path=None,
                 context_path=None,
                 image_tag=None,
                 image_name=None,
                 build_steps=None,
                 env_vars=None,
                 nocache=None,
                 in_cluster_registry=False,
                 k8s_config=None,
                 namespace='default',
                 in_cluster=False,
                 job_container_name=None,
                 job_docker_image=None,
                 job_docker_image_pull_policy=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 use_sidecar=False,
                 sidecar_config=None):
        super().__init__(project_name=project_name,
                         project_uuid=project_uuid,
                         job_name=job_name,
                         job_uuid=job_uuid,
                         spec=spec,
                         commit=commit,
                         from_image=from_image,
                         dockerfile_path=dockerfile_path,
                         context_path=context_path,
                         image_tag=image_tag,
                         image_name=image_name,
                         build_steps=build_steps,
                         env_vars=env_vars,
                         nocache=nocache,
                         in_cluster_registry=in_cluster_registry,
                         k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster,
                         job_container_name=job_container_name,
                         job_docker_image=job_docker_image or conf.get('JOB_KANIKO_IMAGE'),
                         job_docker_image_pull_policy=(
                             job_docker_image_pull_policy or
                             conf.get('JOB_KANIKO_IMAGE_PULL_POLICY')),
                         sidecar_container_name=sidecar_container_name,
                         sidecar_docker_image=sidecar_docker_image,
                         role_label=role_label,
                         type_label=type_label,
                         use_sidecar=use_sidecar,
                         sidecar_config=sidecar_config)

    def get_env_vars(self):
        return None

    def get_pod_command_args(self):
        args = ["-c", constants.BUILD_CONTEXT,
                "-d", "{}:{}".format(self.image_name, self.image_tag)]
        if self.in_cluster_registry:
            args.append(["--insecure"])
        return None, args
