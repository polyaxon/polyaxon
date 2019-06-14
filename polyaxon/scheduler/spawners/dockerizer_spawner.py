from hestia.auth import AuthenticationTypes
from hestia.internal_services import InternalServices
from kubernetes.config import ConfigException

import conf

from constants.k8s_jobs import DOCKERIZER_JOB_NAME
from libs.unique_urls import get_build_health_url
from options.registry.build_jobs import (
    BUILD_JOBS_DOCKER_IMAGE,
    BUILD_JOBS_IMAGE_PULL_POLICY,
    BUILD_JOBS_LANG_ENV,
    BUILD_JOBS_SET_SECURITY_CONTEXT
)
from options.registry.core import SECURITY_CONTEXT_GROUP, SECURITY_CONTEXT_USER
from options.registry.mount_paths import MOUNT_PATHS_NVIDIA
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.dockerizers import manager
from scheduler.spawners.templates.env_vars import get_env_var, get_internal_env_vars
from scheduler.spawners.templates.volumes import (
    get_build_context_volumes,
    get_docker_credentials_volumes,
    get_docker_volumes
)


class DockerizerSpawner(K8SManager):
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
                 insecure=False,
                 creds_secret_ref=None,
                 creds_secret_items=None,
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
        self.spec = spec
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.commit = commit
        self.from_image = from_image
        self.dockerfile_path = dockerfile_path
        self.context_path = context_path
        self.image_tag = image_tag
        self.image_name = image_name
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.nocache = bool(nocache)
        self.insecure = insecure
        self.creds_secret_ref = creds_secret_ref
        self.creds_secret_items = creds_secret_items
        self.resource_manager = manager.ResourceManager(
            namespace=namespace,
            name=DOCKERIZER_JOB_NAME,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            job_name=job_name,
            job_uuid=job_uuid,
            job_docker_image=self.get_job_docker_image(job_docker_image),
            job_docker_image_pull_policy=self.get_job_docker_image_pull_policy(
                job_docker_image_pull_policy),
            job_container_name=job_container_name,
            sidecar_container_name=sidecar_container_name,
            sidecar_docker_image=sidecar_docker_image,
            role_label=role_label,
            type_label=type_label,
            use_sidecar=use_sidecar,
            sidecar_config=sidecar_config,
            health_check_url=get_build_health_url(job_name),
            log_level=self.spec.log_level if self.spec else None)

        super().__init__(k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster)

    @staticmethod
    def get_job_docker_image(job_docker_image):
        return job_docker_image or conf.get(BUILD_JOBS_DOCKER_IMAGE)

    @staticmethod
    def get_job_docker_image_pull_policy(job_docker_image_pull_policy):
        return job_docker_image_pull_policy or conf.get(BUILD_JOBS_IMAGE_PULL_POLICY)

    def get_env_vars(self):
        env_vars = get_internal_env_vars(service_internal_header=InternalServices.DOCKERIZER,
                                         namespace=self.namespace,
                                         authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                         include_internal_token=True)
        # Add set env lang
        get_env_var(name='POLYAXON_LANG_ENV',
                    value=conf.get(BUILD_JOBS_LANG_ENV))
        # Add security context if set
        if conf.get(BUILD_JOBS_SET_SECURITY_CONTEXT):
            get_env_var('POLYAXON_SECURITY_CONTEXT_USER', value=conf.get(SECURITY_CONTEXT_USER))
            get_env_var('POLYAXON_SECURITY_CONTEXT_GROUP', value=conf.get(SECURITY_CONTEXT_GROUP))

        return env_vars

    def get_init_env_vars(self):
        env_vars = get_internal_env_vars(service_internal_header=InternalServices.DOCKERIZER,
                                         namespace=self.namespace,
                                         authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                         include_internal_token=True)
        # Add containers env vars
        env_vars += [
            get_env_var(name='POLYAXON_CONTAINER_BUILD_STEPS', value=self.build_steps),
            get_env_var(name='POLYAXON_CONTAINER_ENV_VARS', value=self.env_vars),
            get_env_var(name='POLYAXON_MOUNT_PATHS_NVIDIA', value=conf.get(MOUNT_PATHS_NVIDIA)),
        ]
        return env_vars

    def get_pod_command_args(self):
        args = ["--build_context={}".format(constants.BUILD_CONTEXT),
                "--image_name={}".format(self.image_name),
                "--image_tag={}".format(self.image_tag)]
        if self.nocache:
            args.append("--nocache")
        return ["python3", "-u", "dockerizer/build_cmd.py"], args

    def get_init_command_args(self):
        return (["python3", "-u", "dockerizer/init_cmd.py"],
                ["--build_context={}".format(constants.BUILD_CONTEXT),
                 "--from_image={}".format(self.from_image or ''),
                 "--dockerfile_path={}".format(self.dockerfile_path or ''),
                 "--context_path={}".format(self.context_path or ''),
                 "--commit={}".format(self.commit or '')])

    def _get_docker_credentials_volumes(self, secret_mount_path: str):
        if not self.creds_secret_ref:
            return [], []
        return get_docker_credentials_volumes(secret_ref=self.creds_secret_ref,
                                              secret_mount_path=secret_mount_path,
                                              secret_items=self.creds_secret_items)

    def get_docker_credentials_volumes(self):
        return self._get_docker_credentials_volumes(secret_mount_path='/root/.docker')

    def start_dockerizer(self,
                         resources=None,
                         node_selector=None,
                         affinity=None,
                         tolerations=None):
        volumes, volume_mounts = get_docker_volumes()
        context_volumes, context_mounts = get_build_context_volumes()
        volumes += context_volumes
        volume_mounts += context_mounts
        registry_auth_volumes, registry_auth_mounts = self.get_docker_credentials_volumes()
        volumes += registry_auth_volumes
        volume_mounts += registry_auth_mounts

        resource_name = self.resource_manager.get_resource_name()
        command, args = self.get_pod_command_args()
        init_command, init_args = self.get_init_command_args()
        pod = self.resource_manager.get_pod(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=self.resource_manager.labels,
            env_vars=self.get_env_vars(),
            command=command,
            args=args,
            init_command=init_command,
            init_args=init_args,
            init_env_vars=self.get_init_env_vars(),
            persistence_outputs=None,
            persistence_data=None,
            outputs_refs_jobs=None,
            outputs_refs_experiments=None,
            secret_refs=None,
            configmap_refs=None,
            resources=resources,
            ephemeral_token=None,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            init_context_mounts=context_mounts,
            restart_policy='Never')

        pod_resp, _ = self.create_or_update_pod(name=resource_name, data=pod)
        return pod_resp.to_dict()

    def stop_dockerizer(self):
        try:
            self.delete_pod(name=self.resource_manager.get_resource_name(), reraise=True)
            return True
        except (PolyaxonK8SError, ConfigException):
            return False
