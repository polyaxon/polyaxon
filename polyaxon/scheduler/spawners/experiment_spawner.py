import uuid

from hestia.auth import AuthenticationTypes
from hestia.internal_services import InternalServices
from kubernetes.config import ConfigException

import conf

from constants.experiment_jobs import get_experiment_job_uuid
from db.redis.ephemeral_tokens import RedisEphemeralTokens
from libs.unique_urls import get_experiment_health_url, get_experiment_reconcile_url
from options.registry.container_names import CONTAINER_NAME_EXPERIMENT_JOBS
from options.registry.restarts import MAX_RESTARTS_EXPERIMENTS
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager
from scheduler.spawners.templates import constants, services
from scheduler.spawners.templates.env_vars import get_internal_env_vars
from scheduler.spawners.templates.experiment_jobs import config_maps, manager
from scheduler.spawners.templates.labels import get_labels
from scheduler.spawners.templates.restart_policy import get_max_restart, get_pod_restart_policy
from scheduler.spawners.templates.volumes import (
    get_auth_context_volumes,
    get_pod_refs_outputs_volumes,
    get_pod_volumes,
    get_shm_volumes
)
from schemas import TaskType


class ExperimentSpawner(K8SManager):
    MASTER_SERVICE = False
    RESOURCE_MANAGER = manager.ResourceManager

    def __init__(self,
                 project_name,
                 experiment_name,
                 project_uuid,
                 experiment_uuid,
                 spec,
                 persistence_config=None,
                 outputs_refs_experiments=None,
                 outputs_refs_jobs=None,
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
                 token_scope=None):
        self.spec = spec
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.experiment_uuid_instance = uuid.UUID(self.experiment_uuid)
        self.original_name = original_name
        self.cloning_strategy = cloning_strategy
        self.persistence_config = persistence_config
        self.outputs_refs_experiments = outputs_refs_experiments
        self.outputs_refs_jobs = outputs_refs_jobs
        self.resource_manager = self.RESOURCE_MANAGER(
            namespace=namespace,
            project_name=self.project_name,
            experiment_group_name=self.experiment_group_name,
            experiment_name=self.experiment_name,
            project_uuid=self.project_uuid,
            experiment_group_uuid=self.experiment_group_uuid,
            experiment_uuid=experiment_uuid,
            job_container_name=self.get_job_container_name(job_container_name),
            job_docker_image=job_docker_image,
            sidecar_container_name=sidecar_container_name,
            sidecar_docker_image=sidecar_docker_image,
            role_label=role_label,
            type_label=type_label,
            use_sidecar=use_sidecar,
            sidecar_config=sidecar_config,
            log_level=self.spec.log_level if self.spec else None,
            original_name=self.original_name,
            cloning_strategy=self.cloning_strategy,
            params=self.spec.params if self.spec else None,
            health_check_url=get_experiment_health_url(self.experiment_name))
        self.token_scope = token_scope
        self.ports = self.get_ports(ports=ports)

        super().__init__(k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster)

        # Set the cluster_def
        cluster_def = self.get_cluster()
        self.resource_manager.set_cluster_def(cluster_def=cluster_def)
        self.job_uuids = self.create_job_uuids()

    def get_ports(self, ports):
        return ports or [constants.DEFAULT_PORT]

    @staticmethod
    def get_job_container_name(job_container_name):
        return job_container_name or conf.get(CONTAINER_NAME_EXPERIMENT_JOBS)

    def create_job_uuids(self):
        return {
            TaskType.MASTER: [
                get_experiment_job_uuid(self.experiment_uuid_instance, 'master', '0')
            ],
        }

    def get_env_vars(self, task_type, task_idx):
        return None

    def get_resources(self, task_type, task_idx):
        return self.spec.master_resources

    def get_labels(self, task_type, task_idx, job_uuid):
        labels = self.resource_manager.get_labels(task_type=task_type,
                                                  task_idx=task_idx,
                                                  job_uuid=job_uuid)

        return get_labels(default_labels=labels, labels=self.spec.master_labels)

    def get_annotations(self, task_type, task_idx):
        return self.spec.master_annotations

    def get_node_selector(self, task_type, task_idx):
        return self.spec.master_node_selector

    def get_affinity(self, task_type, task_idx):
        return self.spec.master_affinity

    def get_tolerations(self, task_type, task_idx):
        return self.spec.master_tolerations

    def get_job_uuids(self, task_type, task_idx):
        return self.job_uuids[task_type][task_idx]

    def get_n_pods(self, task_type):
        return 0

    def get_init_env_vars(self):
        env_vars = get_internal_env_vars(service_internal_header=InternalServices.INITIALIZER,
                                         namespace=self.namespace,
                                         authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                         include_internal_token=True)
        return env_vars

    def _create_job(self,
                    task_type,
                    task_idx,
                    add_service,
                    command=None,
                    args=None,
                    env_vars=None,
                    resources=None,
                    annotations=None,
                    node_selector=None,
                    affinity=None,
                    tolerations=None,
                    max_restarts=None):
        ephemeral_token = None
        if self.token_scope:
            ephemeral_token = RedisEphemeralTokens.generate_header_token(scope=self.token_scope)
        resource_name = self.resource_manager.get_resource_name(task_type=task_type,
                                                                task_idx=task_idx)
        job_uuid = self.get_job_uuids(task_type=task_type, task_idx=task_idx)
        reconcile_url = get_experiment_reconcile_url(self.experiment_name, job_uuid)
        labels = self.get_labels(task_type=task_type,
                                 task_idx=task_idx,
                                 job_uuid=job_uuid)

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

        pod = self.resource_manager.get_task_pod(
            task_type=task_type,
            task_idx=task_idx,
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
            secret_refs=self.spec.secret_refs,
            config_map_refs=self.spec.config_map_refs,
            resources=resources,
            ephemeral_token=ephemeral_token,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            init_context_mounts=context_mounts,
            reconcile_url=reconcile_url,
            max_restarts=max_restarts,
            restart_policy=get_pod_restart_policy(max_restarts))
        pod_resp, _ = self.create_or_update_pod(name=resource_name, body=pod, reraise=True)
        results = {'pod': pod_resp.to_dict()}
        if add_service:
            service = services.get_service(namespace=self.namespace,
                                           name=resource_name,
                                           labels=labels,
                                           ports=self.ports,
                                           target_ports=self.ports)
            service_resp, _ = self.create_or_update_service(name=resource_name,
                                                            body=service,
                                                            reraise=True)
            results['service'] = service_resp.to_dict()
        return results

    def create_multi_jobs(self, task_type, add_service):
        resp = []
        n_pods = self.get_n_pods(task_type=task_type)
        max_restarts = get_max_restart(self.spec.max_restarts, conf.get(MAX_RESTARTS_EXPERIMENTS))
        for i in range(n_pods):
            command, args = self.get_pod_command_args(task_type=task_type, task_idx=i)
            env_vars = self.get_env_vars(task_type=task_type, task_idx=i)
            resources = self.get_resources(task_type=task_type, task_idx=i)
            annotations = self.get_annotations(task_type=task_type, task_idx=i)
            node_selector = self.get_node_selector(task_type=task_type, task_idx=i)
            affinity = self.get_affinity(task_type=task_type, task_idx=i)
            tolerations = self.get_tolerations(task_type=task_type, task_idx=i)
            resp.append(self._create_job(task_type=task_type,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         env_vars=env_vars,
                                         resources=resources,
                                         annotations=annotations,
                                         node_selector=node_selector,
                                         affinity=affinity,
                                         tolerations=tolerations,
                                         add_service=add_service,
                                         max_restarts=max_restarts))
        return resp

    def _delete_job(self, task_type, task_idx, has_service):
        resource_name = self.resource_manager.get_resource_name(task_type=task_type,
                                                                task_idx=task_idx)
        self.delete_pod(name=resource_name, reraise=True)
        if has_service:
            self.delete_service(name=resource_name, reraise=True)

    def delete_multi_jobs(self, task_type, has_service):
        n_pods = self.get_n_pods(task_type=task_type)
        deleted = True
        for i in range(n_pods):
            try:
                self._delete_job(task_type=task_type, task_idx=i, has_service=has_service)
            except (PolyaxonK8SError, ConfigException):
                deleted = False
        return deleted

    def get_pod_command_args(self, task_type, task_idx):
        return self.spec.run.get_container_cmd()

    def create_master(self):
        command, args = self.get_pod_command_args(task_type=TaskType.MASTER, task_idx=0)
        env_vars = self.get_env_vars(task_type=TaskType.MASTER, task_idx=0)
        resources = self.get_resources(task_type=TaskType.MASTER, task_idx=0)
        annotations = self.get_annotations(task_type=TaskType.MASTER, task_idx=0)
        node_selector = self.get_node_selector(task_type=TaskType.MASTER, task_idx=0)
        affinity = self.get_affinity(task_type=TaskType.MASTER, task_idx=0)
        tolerations = self.get_tolerations(task_type=TaskType.MASTER, task_idx=0)
        max_restarts = get_max_restart(self.spec.max_restarts, conf.get(MAX_RESTARTS_EXPERIMENTS))
        return self._create_job(task_type=TaskType.MASTER,
                                task_idx=0,
                                command=command,
                                args=args,
                                env_vars=env_vars,
                                resources=resources,
                                annotations=annotations,
                                node_selector=node_selector,
                                affinity=affinity,
                                tolerations=tolerations,
                                add_service=self.MASTER_SERVICE,
                                max_restarts=max_restarts)

    def delete_master(self):
        try:
            self._delete_job(task_type=TaskType.MASTER, task_idx=0, has_service=self.MASTER_SERVICE)
            return True
        except (PolyaxonK8SError, ConfigException):
            return False

    def create_experiment_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(uuid=self.experiment_uuid)
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
            persistence_outputs=self.persistence_config.outputs,
            params=self.spec.params,
            log_level=self.spec.log_level,
            persistence_data=self.persistence_config.data,
        )

        self.create_or_update_config_map(name=name, body=config_map, reraise=True)

    def delete_experiment_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(uuid=self.experiment_uuid)
        self.delete_config_map(name, reraise=True)

    def delete_experiment_secret(self):
        name = constants.SECRET_NAME.format(uuid=self.experiment_uuid)
        self.delete_secret(name, reraise=True)

    def start_experiment(self):
        master_resp = self.create_master()
        return {
            TaskType.MASTER: master_resp,
        }

    def stop_experiment(self):
        return self.delete_master()

    def _get_pod_address(self, host):
        return '{}:{}'.format(host, self.ports[0])

    def get_cluster(self):
        resource_name = self.resource_manager.get_resource_name(task_type=TaskType.MASTER,
                                                                task_idx=0)
        return {
            TaskType.MASTER: [self._get_pod_address(resource_name)]
        }
