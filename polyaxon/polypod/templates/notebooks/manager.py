import json

from hestia.list_utils import to_list
from kubernetes import client

import conf
import stores

from constants.k8s_jobs import JOB_NAME_FORMAT
from options.registry.affinities import AFFINITIES_NOTEBOOKS
from options.registry.annotations import ANNOTATIONS_NOTEBOOKS
from options.registry.container_names import (
    CONTAINER_NAME_INIT,
    CONTAINER_NAME_PLUGIN_JOBS,
    CONTAINER_NAME_SIDECARS
)
from options.registry.env_vars import ENV_VARS_NOTEBOOKS
from options.registry.init import INIT_DOCKER_IMAGE, INIT_IMAGE_PULL_POLICY
from options.registry.k8s import K8S_RBAC_ENABLED, K8S_SERVICE_ACCOUNT_EXPERIMENTS
from options.registry.k8s_config_maps import K8S_CONFIG_MAPS_NOTEBOOKS
from options.registry.k8s_resources import K8S_RESOURCES_NOTEBOOKS
from options.registry.k8s_secrets import K8S_SECRETS_NOTEBOOKS
from options.registry.node_selectors import NODE_SELECTORS_NOTEBOOKS
from options.registry.service_accounts import SERVICE_ACCOUNTS_NOTEBOOKS
from options.registry.sidecars import SIDECARS_DOCKER_IMAGE, SIDECARS_IMAGE_PULL_POLICY
from options.registry.spawner import APP_LABELS_NOTEBOOK, ROLE_LABELS_DASHBOARD, TYPE_LABELS_RUNNER
from options.registry.tolerations import TOLERATIONS_NOTEBOOKS
from polypod.templates import constants
from polypod.templates.env_vars import get_env_var, get_job_env_vars
from polypod.templates.init_containers import get_auth_context_args
from polypod.templates.pod_environment import (
    get_affinity,
    get_annotations,
    get_config_map_refs,
    get_env_vars,
    get_node_selector,
    get_pod_resources,
    get_secret_refs,
    get_tolerations
)
from polypod.templates.resource_manager import BaseResourceManager
from polypod.templates.resources import get_init_resources


class ResourceManager(BaseResourceManager):
    def __init__(self,
                 namespace,
                 version,
                 name,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 job_docker_image,
                 job_container_name=None,
                 job_docker_image_pull_policy=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 sidecar_docker_image_pull_policy=None,
                 init_container_name=None,
                 init_docker_image=None,
                 init_docker_image_pull_policy=None,
                 role_label=None,
                 type_label=None,
                 app_label=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 health_check_url=None,
                 log_level=None):
        super().__init__(
            namespace=namespace,
            version=version,
            project_name=project_name,
            project_uuid=project_uuid,
            job_container_name=job_container_name or conf.get(CONTAINER_NAME_PLUGIN_JOBS),
            job_docker_image=job_docker_image,
            job_docker_image_pull_policy=job_docker_image_pull_policy,
            sidecar_container_name=sidecar_container_name or conf.get(CONTAINER_NAME_SIDECARS),
            sidecar_docker_image=sidecar_docker_image or conf.get(SIDECARS_DOCKER_IMAGE),
            sidecar_docker_image_pull_policy=(
                sidecar_docker_image_pull_policy or
                conf.get(SIDECARS_IMAGE_PULL_POLICY)),
            init_container_name=init_container_name or conf.get(CONTAINER_NAME_INIT),
            init_docker_image=init_docker_image or conf.get(INIT_DOCKER_IMAGE),  # CHANGE
            init_docker_image_pull_policy=(
                init_docker_image_pull_policy or
                conf.get(INIT_IMAGE_PULL_POLICY)),
            role_label=role_label or conf.get(ROLE_LABELS_DASHBOARD),
            type_label=type_label or conf.get(TYPE_LABELS_RUNNER),
            app_label=app_label or conf.get(APP_LABELS_NOTEBOOK),
            health_check_url=health_check_url,
            use_sidecar=use_sidecar,
            sidecar_config=sidecar_config,
            log_level=log_level
        )
        self.name = name
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.labels = self.get_labels()

    def get_resource_name(self):
        return JOB_NAME_FORMAT.format(name=self.name, job_uuid=self.job_uuid)

    def get_labels(self):
        labels = self.get_recommended_labels(job_uuid=self.job_uuid)
        labels.update({
            'project_name': self.project_name,
            'project_uuid': self.project_uuid,
            'job_name': self.job_name,
            'job_uuid': self.job_uuid,
            'role': self.role_label,
            'type': self.type_label,
            'app': self.app_label
        })
        return labels

    def _get_logs_path(self, persistence_logs='default'):
        return stores.get_job_logs_path(
            persistence=persistence_logs,
            job_name=self.job_name,
            temp=False)

    def _get_outputs_path(self, persistence_outputs):
        return stores.get_job_outputs_path(
            persistence=persistence_outputs,
            job_name=self.job_name)

    def _get_container_pod_env_vars(self,
                                    persistence_outputs,
                                    persistence_data,
                                    outputs_refs_jobs,
                                    outputs_refs_experiments,
                                    ephemeral_token):
        logs_path = self._get_logs_path()
        outputs_path = self._get_outputs_path(persistence_outputs=persistence_outputs)
        env_vars = get_job_env_vars(
            namespace=self.namespace,
            persistence_outputs=persistence_outputs,
            outputs_path=outputs_path,
            persistence_data=persistence_data,
            log_level=self.log_level,
            logs_path=logs_path,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            ephemeral_token=ephemeral_token,
        )
        return env_vars + [
            get_env_var(name=constants.CONFIG_MAP_NOTEBOOK_INFO_KEY_NAME,
                        value=json.dumps(self.labels)),
        ]

    def get_init_container(self,
                           init_command,
                           init_args,
                           env_vars,
                           context_mounts,
                           persistence_outputs,
                           persistence_data):
        """Pod init container for setting outputs path."""
        env_vars = to_list(env_vars, check_none=True)
        volume_mounts = to_list(context_mounts, check_none=True)
        init_command = init_command or ["/bin/sh", "-c"]
        init_args = to_list(get_auth_context_args(entity='notebook', entity_name=self.job_name))
        return client.V1Container(
            name=self.init_container_name,
            image=self.init_docker_image,
            image_pull_policy=self.init_docker_image_pull_policy,
            command=init_command,
            args=init_args,
            env=env_vars,
            resources=get_init_resources(),
            volume_mounts=volume_mounts)

    def _get_pod_resources(self, resources):
        return get_pod_resources(
            resources=resources,
            default_resources=conf.get(K8S_RESOURCES_NOTEBOOKS))

    def _get_annotations(self, annotations):
        return get_annotations(
            annotations=annotations,
            default_annotations=conf.get(ANNOTATIONS_NOTEBOOKS))

    def _get_node_selector(self, node_selector):
        return get_node_selector(
            node_selector=node_selector,
            default_node_selector=conf.get(NODE_SELECTORS_NOTEBOOKS))

    def _get_affinity(self, affinity):
        return get_affinity(
            affinity=affinity,
            default_affinity=conf.get(AFFINITIES_NOTEBOOKS))

    def _get_tolerations(self, tolerations):
        return get_tolerations(
            tolerations=tolerations,
            default_tolerations=conf.get(TOLERATIONS_NOTEBOOKS))

    def _get_service_account_name(self):
        service_account_name = None
        sa = conf.get(SERVICE_ACCOUNTS_NOTEBOOKS)
        if not sa:
            sa = conf.get(K8S_SERVICE_ACCOUNT_EXPERIMENTS)
        if conf.get(K8S_RBAC_ENABLED) and sa:
            service_account_name = sa
        return service_account_name

    def _get_secret_refs(self, secret_refs):
        return get_secret_refs(
            secret_refs=secret_refs,
            default_secret_refs=conf.get(K8S_SECRETS_NOTEBOOKS))

    def _get_config_map_refs(self, config_map_refs):
        return get_config_map_refs(
            config_map_refs=config_map_refs,
            default_config_map_refs=conf.get(K8S_CONFIG_MAPS_NOTEBOOKS))

    def _get_kv_env_vars(self, env_vars):
        return get_env_vars(
            env_vars=env_vars,
            default_env_vars=conf.get(ENV_VARS_NOTEBOOKS))
