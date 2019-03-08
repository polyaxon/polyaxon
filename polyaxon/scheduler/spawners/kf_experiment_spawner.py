from constants.k8s_jobs import EXPERIMENT_KF_JOB_NAME_FORMAT
from db.redis.ephemeral_tokens import RedisEphemeralTokens
from polyaxon_k8s.exceptions import PolyaxonK8SError
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.templates.env_vars import validate_configmap_refs, validate_secret_refs
from scheduler.spawners.templates.kf_jobs import manager
from scheduler.spawners.templates.kubeflow import KUBEFLOW_JOB_GROUP
from scheduler.spawners.templates.volumes import (
    get_auth_context_volumes,
    get_pod_refs_outputs_volumes,
    get_pod_volumes,
    get_shm_volumes
)
from schemas.tasks import TaskType


class KFExperimentSpawner(ExperimentSpawner):
    MASTER_SERVICE = False
    RESOURCE_MANAGER = manager.ResourceManager
    KIND = None
    VERSION = None
    PLURAL = None
    SPEC = None

    @property
    def api_version(self):
        return '{}/{}'.format(KUBEFLOW_JOB_GROUP, self.VERSION)

    def _create_job(self,  # pylint:disable=arguments-differ
                    task_type,
                    command=None,
                    args=None,
                    env_vars=None,
                    resources=None,
                    node_selector=None,
                    affinity=None,
                    tolerations=None,
                    replicas=1,
                    restart_policy='Never'):
        ephemeral_token = None
        if self.token_scope:
            ephemeral_token = RedisEphemeralTokens.generate_header_token(scope=self.token_scope)
        resource_name = self.resource_manager.get_kf_resource_name(task_type=task_type)
        labels = self.resource_manager.get_labels(task_type=task_type)

        # Set and validate volumes
        volumes, volume_mounts = get_pod_volumes(
            persistence_outputs=self.persistence_config.outputs,
            persistence_data=self.persistence_config.data)
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=self.outputs_refs_jobs,
            persistence_outputs=self.persistence_config.outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=self.outputs_refs_experiments,
            persistence_outputs=self.persistence_config.outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        shm_volumes, shm_volume_mounts = get_shm_volumes()
        volumes += shm_volumes
        volume_mounts += shm_volume_mounts

        context_volumes, context_mounts = get_auth_context_volumes()
        volumes += context_volumes
        volume_mounts += context_mounts

        # Validate secret and configmap refs
        secret_refs = validate_secret_refs(self.spec.secret_refs)
        configmap_refs = validate_configmap_refs(self.spec.configmap_refs)

        pod_template_spec = self.resource_manager.get_pod_template_spec(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=labels,
            env_vars=env_vars,
            command=command,
            args=args,
            ports=self.ports,
            init_env_vars=self.get_init_env_vars(),
            persistence_outputs=self.persistence_config.outputs,
            persistence_data=self.persistence_config.data,
            outputs_refs_jobs=self.outputs_refs_jobs,
            outputs_refs_experiments=self.outputs_refs_experiments,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            resources=resources,
            ephemeral_token=ephemeral_token,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            init_context_mounts=context_mounts,
            restart_policy=restart_policy)
        return {
            'replicas': replicas,
            'restartPolicy': restart_policy,
            'template': pod_template_spec
        }

    def create_multi_jobs(self, task_type):  # pylint:disable=arguments-differ
        n_pods = self.get_n_pods(task_type=task_type)
        command, args = self.get_pod_command_args(task_type=task_type, task_idx=0)
        env_vars = self.get_env_vars(task_type=task_type, task_idx=0)
        resources = self.get_resources(task_type=task_type, task_idx=0)
        node_selector = self.get_node_selector(task_type=task_type, task_idx=0)
        affinity = self.get_affinity(task_type=task_type, task_idx=0)
        tolerations = self.get_tolerations(task_type=task_type, task_idx=0)
        return self._create_job(task_type=task_type,
                                command=command,
                                args=args,
                                env_vars=env_vars,
                                resources=resources,
                                node_selector=node_selector,
                                affinity=affinity,
                                tolerations=tolerations,
                                replicas=n_pods)

    def create_master(self):
        command, args = self.get_pod_command_args(task_type=TaskType.MASTER, task_idx=0)
        env_vars = self.get_env_vars(task_type=TaskType.MASTER, task_idx=0)
        resources = self.get_resources(task_type=TaskType.MASTER, task_idx=0)
        node_selector = self.get_node_selector(task_type=TaskType.MASTER, task_idx=0)
        affinity = self.get_affinity(task_type=TaskType.MASTER, task_idx=0)
        tolerations = self.get_tolerations(task_type=TaskType.MASTER, task_idx=0)
        return self._create_job(task_type=TaskType.MASTER,
                                command=command,
                                args=args,
                                env_vars=env_vars,
                                resources=resources,
                                node_selector=node_selector,
                                affinity=affinity,
                                tolerations=tolerations)

    def delete_master(self):
        try:
            self._delete_job(task_type=TaskType.MASTER, task_idx=0, has_service=self.MASTER_SERVICE)
            return True
        except PolyaxonK8SError:
            return False

    def stop_experiment(self):
        resource_name = EXPERIMENT_KF_JOB_NAME_FORMAT.format(
            experiment_uuid=self.resource_manager.experiment_uuid)
        try:
            self.delete_custom_object(name=resource_name,
                                      group=KUBEFLOW_JOB_GROUP,
                                      version=self.VERSION,
                                      plural=self.PLURAL)
            return True
        except PolyaxonK8SError:
            return False
