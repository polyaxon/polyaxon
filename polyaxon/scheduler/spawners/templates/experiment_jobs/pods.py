import json
import uuid

from kubernetes import client

from django.conf import settings

from db.models.cloning_strategies import CloningStrategy
from libs.paths.data_paths import get_data_paths
from libs.paths.experiments import get_experiment_logs_path, get_experiment_outputs_path
from libs.utils import get_list
from polyaxon_k8s import constants as k8s_constants
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.utils import to_list
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import (
    get_env_var,
    get_job_env_vars,
    get_resources_env_vars
)
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.init_containers import InitCommands, get_output_args
from scheduler.spawners.templates.node_selectors import get_node_selector
from scheduler.spawners.templates.resources import get_resources
from scheduler.spawners.templates.sidecars import get_sidecar_container
from scheduler.spawners.templates.volumes import get_pod_outputs_volume


class PodManager(object):
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
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 init_container_name=None,
                 init_docker_image=None,
                 role_label=None,
                 type_label=None,
                 ports=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 log_level=None,
                 declarations=None):
        self.namespace = namespace
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.original_name = original_name
        self.cloning_strategy = cloning_strategy
        self.job_container_name = job_container_name or settings.CONTAINER_NAME_EXPERIMENT_JOB
        self.job_docker_image = job_docker_image or settings.JOB_DOCKER_NAME
        self.sidecar_container_name = sidecar_container_name or settings.CONTAINER_NAME_SIDECAR
        self.sidecar_docker_image = sidecar_docker_image or settings.JOB_SIDECAR_DOCKER_IMAGE
        self.init_container_name = init_container_name or settings.CONTAINER_NAME_INIT
        self.init_docker_image = init_docker_image or settings.JOB_INIT_DOCKER_IMAGE
        self.role_label = role_label or settings.ROLE_LABELS_WORKER
        self.type_label = type_label or settings.TYPE_LABELS_EXPERIMENT
        self.app_label = settings.APP_LABELS_EXPERIMENT
        self.ports = ports or [constants.DEFAULT_PORT]
        self.use_sidecar = use_sidecar
        if use_sidecar and not sidecar_config:
            raise PolyaxonConfigurationError(
                'In order to use a `sidecar_config` is required. '
                'The `sidecar_config` must correspond to the sidecar docker image used.')
        self.sidecar_config = sidecar_config
        self.log_level = log_level
        self.declarations = declarations
        self.experiment_labels = self.get_experiment_labels()
        self.cluster_def = None

    def set_cluster_def(self, cluster_def):
        self.cluster_def = cluster_def

    def get_job_name(self, task_type, task_idx):
        return constants.EXPERIMENT_JOB_NAME.format(task_type=task_type,
                                                    task_idx=task_idx,
                                                    experiment_uuid=self.experiment_uuid)

    def get_experiment_labels(self):
        labels = {'project_name': self.project_name,
                  'experiment_group_name': self.experiment_group_name,
                  'experiment_name': self.experiment_name,
                  'project_uuid': self.project_uuid,
                  'experiment_uuid': self.experiment_uuid}
        if self.experiment_group_uuid:
            labels['experiment_group_uuid'] = self.experiment_group_uuid

        return labels

    def get_labels(self, task_type, task_idx):
        labels = self.get_experiment_labels()
        labels.update({
            'task_type': task_type,
            'task_idx': '{}'.format(task_idx),
            'job_uuid': uuid.uuid4().hex,
            'role': self.role_label,
            'type': self.type_label
        })
        return labels

    def get_pod_container(self,
                          volume_mounts,
                          env_vars=None,
                          command=None,
                          args=None,
                          persistence_outputs=None,
                          persistence_data=None,
                          resources=None):
        """Pod job container for task."""
        assert self.cluster_def is not None

        env_vars = get_list(env_vars)
        outputs_path = get_experiment_outputs_path(
            persistence_outputs=persistence_outputs,
            experiment_name=self.experiment_name,
            original_name=self.original_name,
            cloning_strategy=self.cloning_strategy)
        env_vars += get_job_env_vars(
            log_level=self.log_level,
            outputs_path=outputs_path,
            data_paths=get_data_paths(persistence_data),
            logs_path=get_experiment_logs_path(self.experiment_name),
        )
        env_vars += [
            get_env_var(name=constants.CONFIG_MAP_CLUSTER_KEY_NAME,
                        value=json.dumps(self.cluster_def)),
            get_env_var(name=constants.CONFIG_MAP_DECLARATIONS_KEY_NAME,
                        value=self.declarations),
            get_env_var(name=constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME,
                        value=json.dumps(self.experiment_labels)),
        ]

        env_vars += get_resources_env_vars(resources=resources)

        ports = [client.V1ContainerPort(container_port=port) for port in self.ports]
        return client.V1Container(name=self.job_container_name,
                                  image=self.job_docker_image,
                                  command=command,
                                  args=args,
                                  ports=ports,
                                  env=env_vars,
                                  resources=get_resources(resources),
                                  volume_mounts=volume_mounts)

    def get_sidecar_container(self, task_type, task_idx, args):
        """Pod sidecar container for task logs."""
        return get_sidecar_container(
            job_name=self.get_job_name(task_type=task_type, task_idx=task_idx),
            job_container_name=self.job_container_name,
            sidecar_container_name=self.sidecar_container_name,
            sidecar_docker_image=self.sidecar_docker_image,
            namespace=self.namespace,
            app_label=self.app_label,
            sidecar_config=self.sidecar_config,
            sidecar_args=args)

    def get_init_container(self, persistence_outputs):
        """Pod init container for setting outputs path."""
        if self.original_name is not None and self.cloning_strategy == CloningStrategy.RESUME:
            return []
        if self.original_name is not None and self.cloning_strategy == CloningStrategy.COPY:
            command = InitCommands.COPY
            original_outputs_path = get_experiment_outputs_path(
                persistence_outputs=persistence_outputs, experiment_name=self.original_name)
        else:
            command = InitCommands.CREATE
            original_outputs_path = None

        outputs_path = get_experiment_outputs_path(persistence_outputs=persistence_outputs,
                                                   experiment_name=self.experiment_name)
        _, outputs_volume_mount = get_pod_outputs_volume(persistence_outputs=persistence_outputs)
        return [
            client.V1Container(
                name=self.init_container_name,
                image=self.init_docker_image,
                command=["/bin/sh", "-c"],
                args=to_list(get_output_args(command=command,
                                             outputs_path=outputs_path,
                                             original_outputs_path=original_outputs_path)),
                volume_mounts=outputs_volume_mount)
        ]

    def get_task_pod_spec(self,
                          task_type,
                          task_idx,
                          volume_mounts,
                          volumes,
                          env_vars=None,
                          command=None,
                          args=None,
                          sidecar_args=None,
                          persistence_outputs=None,
                          persistence_data=None,
                          resources=None,
                          node_selector=None,
                          restart_policy='OnFailure'):
        """Pod spec to be used to create pods for tasks: master, worker, ps."""
        volume_mounts = get_list(volume_mounts)
        volumes = get_list(volumes)

        gpu_volume_mounts, gpu_volumes = get_gpu_volumes_def(resources)
        volume_mounts += gpu_volume_mounts
        volumes += gpu_volumes

        # Add job information
        env_vars = get_list(env_vars)
        env_vars.append(
            client.V1EnvVar(
                name=constants.CONFIG_MAP_TASK_INFO_KEY_NAME,
                value=json.dumps({'type': task_type, 'index': task_idx})
            )
        )

        pod_container = self.get_pod_container(volume_mounts=volume_mounts,
                                               env_vars=env_vars,
                                               command=command,
                                               args=args,
                                               persistence_outputs=persistence_outputs,
                                               persistence_data=persistence_data,
                                               resources=resources)

        containers = [pod_container]
        if self.use_sidecar:
            sidecar_container = self.get_sidecar_container(task_type=task_type,
                                                           task_idx=task_idx,
                                                           args=sidecar_args)
            containers.append(sidecar_container)

        node_selector = get_node_selector(
            node_selector=node_selector,
            default_node_selector=settings.NODE_SELECTORS_EXPERIMENTS)
        service_account_name = None
        if settings.K8S_RBAC_ENABLED:
            service_account_name = settings.K8S_SERVICE_ACCOUNT_NAME
        return client.V1PodSpec(
            restart_policy=restart_policy,
            service_account_name=service_account_name,
            init_containers=to_list(self.get_init_container(persistence_outputs)),
            containers=containers,
            volumes=volumes,
            node_selector=node_selector)

    def get_pod(self,
                task_type,
                task_idx,
                volume_mounts,
                volumes,
                labels,
                env_vars=None,
                command=None,
                args=None,
                sidecar_args=None,
                persistence_outputs=None,
                persistence_data=None,
                resources=None,
                node_selector=None,
                restart_policy=None):
        job_name = self.get_job_name(task_type=task_type, task_idx=task_idx)
        metadata = client.V1ObjectMeta(name=job_name, labels=labels, namespace=self.namespace)

        pod_spec = self.get_task_pod_spec(
            task_type=task_type,
            task_idx=task_idx,
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            sidecar_args=sidecar_args,
            persistence_outputs=persistence_outputs,
            persistence_data=persistence_data,
            resources=resources,
            node_selector=node_selector,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)

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
