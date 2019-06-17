import json

from hestia.list_utils import to_list
from kubernetes import client

import conf
import stores

from constants.cloning_strategies import CloningStrategy
from constants.k8s_jobs import EXPERIMENT_JOB_NAME_FORMAT
from options.registry.affinities import AFFINITIES_EXPERIMENTS
from options.registry.container_names import CONTAINER_NAME_INIT, CONTAINER_NAME_SIDECARS
from options.registry.init import INIT_DOCKER_IMAGE, INIT_IMAGE_PULL_POLICY
from options.registry.k8s import K8S_RBAC_ENABLED, K8S_SERVICE_ACCOUNT_EXPERIMENTS
from options.registry.k8s_config_maps import K8S_CONFIG_MAPS_EXPERIMENTS
from options.registry.k8s_resources import K8S_RESOURCES_EXPERIMENTS
from options.registry.k8s_secrets import K8S_SECRETS_EXPERIMENTS
from options.registry.node_selectors import NODE_SELECTORS_EXPERIMENTS
from options.registry.service_accounts import SERVICE_ACCOUNTS_EXPERIMENTS
from options.registry.sidecars import SIDECARS_DOCKER_IMAGE, SIDECARS_IMAGE_PULL_POLICY
from options.registry.spawner import APP_LABELS_EXPERIMENT, ROLE_LABELS_WORKER, TYPE_LABELS_RUNNER
from options.registry.tolerations import TOLERATIONS_EXPERIMENTS
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_env_var, get_job_env_vars
from scheduler.spawners.templates.init_containers import (
    InitCommands,
    get_auth_context_args,
    get_output_args
)
from scheduler.spawners.templates.pod_environment import (
    get_affinity,
    get_config_map_refs,
    get_node_selector,
    get_pod_resources,
    get_secret_refs,
    get_tolerations
)
from scheduler.spawners.templates.resource_manager import BaseResourceManager
from scheduler.spawners.templates.resources import get_init_resources
from scheduler.spawners.templates.volumes import get_pod_outputs_volume


class ResourceManager(BaseResourceManager):
    def __init__(self,
                 namespace,
                 project_name,
                 experiment_group_name,
                 experiment_name,
                 project_uuid,
                 experiment_group_uuid,
                 experiment_uuid,
                 original_name=None,
                 cloning_strategy=None,
                 job_container_name=None,
                 job_docker_image=None,
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
                 health_check_url=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 log_level=None,
                 declarations=None):
        super().__init__(
            namespace=namespace,
            project_name=project_name,
            project_uuid=project_uuid,
            job_container_name=job_container_name,
            job_docker_image=job_docker_image,
            job_docker_image_pull_policy=job_docker_image_pull_policy,
            sidecar_container_name=sidecar_container_name or conf.get(CONTAINER_NAME_SIDECARS),
            sidecar_docker_image=sidecar_docker_image or conf.get(SIDECARS_DOCKER_IMAGE),
            sidecar_docker_image_pull_policy=(
                sidecar_docker_image_pull_policy or
                conf.get(SIDECARS_IMAGE_PULL_POLICY)),
            init_container_name=init_container_name or conf.get(CONTAINER_NAME_INIT),
            init_docker_image=init_docker_image or conf.get(INIT_DOCKER_IMAGE),
            init_docker_image_pull_policy=(
                init_docker_image_pull_policy or
                conf.get(INIT_IMAGE_PULL_POLICY)),
            role_label=role_label or conf.get(ROLE_LABELS_WORKER),
            type_label=type_label or conf.get(TYPE_LABELS_RUNNER),
            app_label=app_label or conf.get(APP_LABELS_EXPERIMENT),
            health_check_url=health_check_url,
            use_sidecar=use_sidecar,
            sidecar_config=sidecar_config,
            log_level=log_level,
        )
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.original_name = original_name
        self.cloning_strategy = cloning_strategy
        self.declarations = declarations
        self.experiment_labels = self.get_experiment_labels()
        self.cluster_def = None

    def set_cluster_def(self, cluster_def):
        self.cluster_def = cluster_def

    def get_resource_name(self, task_type, task_idx):  # pylint:disable=arguments-differ
        return EXPERIMENT_JOB_NAME_FORMAT.format(task_type=task_type,
                                                 task_idx=task_idx,
                                                 experiment_uuid=self.experiment_uuid)

    def get_experiment_labels(self):
        labels = {
            'role': self.role_label,
            'type': self.type_label,
            'app': self.app_label,
            'project_name': self.project_name,
            'experiment_group_name': self.experiment_group_name,
            'experiment_name': self.experiment_name,
            'project_uuid': self.project_uuid,
            'experiment_uuid': self.experiment_uuid
        }
        if self.experiment_group_uuid:
            labels['experiment_group_uuid'] = self.experiment_group_uuid

        return labels

    def get_labels(self, task_type, task_idx, job_uuid):  # pylint:disable=arguments-differ
        labels = self.get_recommended_labels(job_uuid=job_uuid)
        labels.update(self.get_experiment_labels())
        labels.update({
            'task_type': task_type,
            'task_idx': '{}'.format(task_idx),
            'job_uuid': job_uuid
        })
        return labels

    def _pod_container_checks(self):
        assert self.cluster_def is not None

    def _get_logs_path(self, persistence_logs='default'):
        return stores.get_experiment_logs_path(
            persistence=persistence_logs,
            experiment_name=self.experiment_name,
            temp=False)

    def _get_outputs_path(self, persistence_outputs):
        return stores.get_experiment_outputs_path(
            persistence=persistence_outputs,
            experiment_name=self.experiment_name,
            original_name=self.original_name,
            cloning_strategy=self.cloning_strategy)

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
            get_env_var(name=constants.CONFIG_MAP_CLUSTER_KEY_NAME,
                        value=json.dumps(self.cluster_def)),
            get_env_var(name=constants.CONFIG_MAP_DECLARATIONS_KEY_NAME,
                        value=self.declarations),
            get_env_var(name=constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME,
                        value=json.dumps(self.experiment_labels)),
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
        if self.original_name is not None and self.cloning_strategy == CloningStrategy.RESUME:
            return []
        if self.original_name is not None and self.cloning_strategy == CloningStrategy.COPY:
            command = InitCommands.COPY
            original_outputs_path = stores.get_experiment_outputs_path(
                persistence=persistence_outputs,
                experiment_name=self.original_name)
        else:
            command = InitCommands.CREATE
            original_outputs_path = None

        outputs_path = stores.get_experiment_outputs_path(
            persistence=persistence_outputs,
            experiment_name=self.experiment_name)
        _, outputs_volume_mount = get_pod_outputs_volume(persistence_outputs=persistence_outputs)
        volume_mounts = outputs_volume_mount + to_list(context_mounts, check_none=True)
        init_command = init_command or ["/bin/sh", "-c"]
        init_args = init_args or to_list(
            get_output_args(command=command,
                            outputs_path=outputs_path,
                            original_outputs_path=original_outputs_path))
        init_args += to_list(get_auth_context_args(entity='experiment',
                                                   entity_name=self.experiment_name))
        return [
            client.V1Container(
                name=self.init_container_name,
                image=self.init_docker_image,
                image_pull_policy=self.init_docker_image_pull_policy,
                command=init_command,
                args=[''.join(init_args)],
                env=env_vars,
                resources=get_init_resources(),
                volume_mounts=volume_mounts)
        ]

    def _get_pod_resources(self, resources):
        return get_pod_resources(
            resources=resources,
            default_resources=conf.get(K8S_RESOURCES_EXPERIMENTS))

    def _get_node_selector(self, node_selector):
        return get_node_selector(
            node_selector=node_selector,
            default_node_selector=conf.get(NODE_SELECTORS_EXPERIMENTS))

    def _get_affinity(self, affinity):
        return get_affinity(
            affinity=affinity,
            default_affinity=conf.get(AFFINITIES_EXPERIMENTS))

    def _get_tolerations(self, tolerations):
        return get_tolerations(
            tolerations=tolerations,
            default_tolerations=conf.get(TOLERATIONS_EXPERIMENTS))

    def _get_secret_refs(self, secret_refs):
        return get_secret_refs(
            secret_refs=secret_refs,
            default_secret_refs=conf.get(K8S_SECRETS_EXPERIMENTS))

    def _get_config_map_refs(self, config_map_refs):
        return get_config_map_refs(
            config_map_refs=config_map_refs,
            default_config_map_refs=conf.get(K8S_CONFIG_MAPS_EXPERIMENTS))

    def _get_service_account_name(self):
        service_account_name = None
        sa = conf.get(SERVICE_ACCOUNTS_EXPERIMENTS)
        if not sa:
            sa = conf.get(K8S_SERVICE_ACCOUNT_EXPERIMENTS)
        if conf.get(K8S_RBAC_ENABLED) and sa:
            service_account_name = sa
        return service_account_name

    def get_task_pod(self,
                     task_type,
                     task_idx,
                     volume_mounts,
                     volumes,
                     labels,
                     env_vars=None,
                     init_env_vars=None,
                     command=None,
                     args=None,
                     ports=None,
                     persistence_outputs=None,
                     persistence_data=None,
                     outputs_refs_jobs=None,
                     outputs_refs_experiments=None,
                     secret_refs=None,
                     config_map_refs=None,
                     resources=None,
                     ephemeral_token=None,
                     node_selector=None,
                     affinity=None,
                     tolerations=None,
                     sidecar_context_mounts=None,
                     init_context_mounts=None,
                     restart_policy=None):
        resource_name = self.get_resource_name(task_type=task_type, task_idx=task_idx)
        env_vars = to_list(env_vars, check_none=True)
        env_vars.append(
            client.V1EnvVar(
                name=constants.CONFIG_MAP_TASK_INFO_KEY_NAME,
                value=json.dumps({'type': task_type, 'index': task_idx})
            )
        )

        return self.get_pod(resource_name=resource_name,
                            volume_mounts=volume_mounts,
                            volumes=volumes,
                            labels=labels,
                            env_vars=env_vars,
                            command=command,
                            args=args,
                            init_env_vars=init_env_vars,
                            ports=ports,
                            persistence_outputs=persistence_outputs,
                            persistence_data=persistence_data,
                            outputs_refs_jobs=outputs_refs_jobs,
                            outputs_refs_experiments=outputs_refs_experiments,
                            secret_refs=secret_refs,
                            config_map_refs=config_map_refs,
                            resources=resources,
                            ephemeral_token=ephemeral_token,
                            node_selector=node_selector,
                            affinity=affinity,
                            tolerations=tolerations,
                            sidecar_context_mounts=sidecar_context_mounts,
                            init_context_mounts=init_context_mounts,
                            restart_policy=restart_policy)

    def _get_from_experiment_config_map(self, key_name):
        name = constants.CONFIG_MAP_NAME.format(uuid=self.experiment_uuid)
        config_map_key_ref = client.V1ConfigMapKeySelector(name=name, key=key_name)
        value = client.V1EnvVarSource(config_map_key_ref=config_map_key_ref)
        return client.V1EnvVar(name=key_name, value_from=value)

    def _get_from_experiment_secret(self, key_name):
        name = constants.SECRET_NAME.format(uuid=self.experiment_uuid)
        secret_key_ref = client.V1SecretKeySelector(name=name, key=key_name)
        value = client.V1EnvVarSource(secret_key_ref=secret_key_ref)
        return client.V1EnvVar(name=key_name, value_from=value)
