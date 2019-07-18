from typing import List, Optional, Tuple

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
from polypod.templates import constants
from polypod.templates.dockerizers import manager
from polypod.templates.env_vars import get_internal_env_vars, get_str_var
from polypod.templates.labels import get_labels
from polypod.templates.restart_policy import get_pod_restart_policy
from polypod.templates.volumes import (
    get_build_context_volumes,
    get_docker_credentials_volumes,
    get_docker_volumes
)


class DockerizerSpawner(K8SManager):
    SECRET_MOUNT_PATH = '/root/.docker'

    def __init__(self,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 k8s_config=None,
                 namespace='default',
                 version=None,
                 in_cluster=False,
                 job_container_name=None,
                 job_docker_image=None,
                 job_docker_image_pull_policy=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 log_level=None):
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.resource_manager = manager.ResourceManager(
            namespace=namespace,
            version=version,
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
            log_level=log_level)

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
        return get_internal_env_vars(service_internal_header=InternalServices.DOCKERIZER,
                                     namespace=self.namespace,
                                     authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                     include_internal_token=True)

    def get_init_env_vars(self):
        env_vars = get_internal_env_vars(service_internal_header=InternalServices.DOCKERIZER,
                                         namespace=self.namespace,
                                         authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                         include_internal_token=True)
        return env_vars

    def get_pod_command_args(self, image_name, image_tag, nocache, insecure):
        args = ["--build_context={}".format(constants.BUILD_CONTEXT),
                "--image_name={}".format(image_name),
                "--image_tag={}".format(image_tag)]
        if bool(nocache):
            args.append("--nocache")
        return ["python3", "-u", "dockerizer/build_cmd.py"], args

    @staticmethod
    def get_init_command_args(from_image,
                              dockerfile_path,
                              lang_env,
                              context_path,
                              commit,
                              env_vars,
                              build_steps):
        # Add security context if set
        uid = conf.get(SECURITY_CONTEXT_USER)
        gid = conf.get(SECURITY_CONTEXT_GROUP)
        should_set_security_context = conf.get(BUILD_JOBS_SET_SECURITY_CONTEXT) and uid and gid
        lang_env = lang_env or conf.get(BUILD_JOBS_LANG_ENV)
        mount_paths_nvidia = conf.get(MOUNT_PATHS_NVIDIA).get('nvidia-bin')

        args = [
            "--build_context={}".format(constants.BUILD_CONTEXT),
            "--from_image={}".format(from_image or ''),
            "--dockerfile_path={}".format(dockerfile_path or ''),
            "--context_path={}".format(context_path or ''),
            "--commit={}".format(commit or ''),
        ]
        if should_set_security_context:
            args += ["--uid={}".format(uid), "--gid={}".format(gid)]
        if lang_env:
            args.append("--lang_env={}".format(lang_env))
        if env_vars:
            args.append("--env_vars={}".format(get_str_var(env_vars)))
        if mount_paths_nvidia:
            args.append("--mount_paths_nvidia={}".format(get_str_var(mount_paths_nvidia)))
        if build_steps:
            args.append("--build_steps={}".format(get_str_var(build_steps)))

        return ["python3", "-u", "dockerizer/init_cmd.py"], args

    def get_docker_credentials_volumes(self, secret_ref: str, secret_items: List[str]):
        if not secret_ref:
            return [], []
        return get_docker_credentials_volumes(secret_ref=secret_ref,
                                              secret_mount_path=self.SECRET_MOUNT_PATH,
                                              secret_items=secret_items)

    def start_dockerizer(self,
                         image_name: str,
                         image_tag: str,
                         from_image: str,
                         nocache: bool,
                         dockerfile_path: str,
                         lang_env: str,
                         context_path: str,
                         commit: str,
                         env_vars: Optional[List[Tuple[str, str]]],
                         build_steps: Optional[List[str]],
                         insecure: bool,
                         creds_secret_ref: str,
                         creds_secret_items: List[str],
                         secret_refs=None,
                         config_map_refs=None,
                         resources=None,
                         labels=None,
                         annotations=None,
                         node_selector=None,
                         affinity=None,
                         tolerations=None,
                         reconcile_url=None,
                         max_restarts=None):
        volumes, volume_mounts = get_docker_volumes()
        context_volumes, context_mounts = get_build_context_volumes()
        volumes += context_volumes
        volume_mounts += context_mounts
        registry_auth_volumes, registry_auth_mounts = self.get_docker_credentials_volumes(
            secret_ref=creds_secret_ref,
            secret_items=creds_secret_items
        )
        volumes += registry_auth_volumes
        volume_mounts += registry_auth_mounts

        resource_name = self.resource_manager.get_resource_name()
        command, args = self.get_pod_command_args(image_name=image_name,
                                                  image_tag=image_tag,
                                                  nocache=nocache,
                                                  insecure=insecure)
        init_command, init_args = self.get_init_command_args(
            from_image=from_image,
            dockerfile_path=dockerfile_path,
            lang_env=lang_env,
            context_path=context_path,
            commit=commit,
            env_vars=env_vars,
            build_steps=build_steps,
        )

        labels = get_labels(default_labels=self.resource_manager.labels, labels=labels)
        pod = self.resource_manager.get_pod(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=labels,
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
            secret_refs=secret_refs,
            config_map_refs=config_map_refs,
            resources=resources,
            annotations=annotations,
            ephemeral_token=None,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            init_context_mounts=context_mounts,
            reconcile_url=reconcile_url,
            max_restarts=max_restarts,
            restart_policy=get_pod_restart_policy(max_restarts))

        pod_resp, _ = self.create_or_update_pod(name=resource_name, body=pod, reraise=True)
        return pod_resp.to_dict()

    def stop_dockerizer(self):
        try:
            self.delete_pod(name=self.resource_manager.get_resource_name(), reraise=True)
            return True
        except (PolyaxonK8SError, ConfigException):
            return False
