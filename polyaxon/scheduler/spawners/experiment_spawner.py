from db.redis.ephemeral_tokens import RedisEphemeralTokens
from libs.unique_urls import get_experiment_health_url
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager
from scheduler.spawners.templates import constants, services
from scheduler.spawners.templates.base_pods import get_pod_command_args
from scheduler.spawners.templates.env_vars import validate_configmap_refs, validate_secret_refs
from scheduler.spawners.templates.experiment_jobs import config_maps, pods
from scheduler.spawners.templates.sidecars import get_sidecar_args
from scheduler.spawners.templates.volumes import (
    get_pod_refs_outputs_volumes,
    get_pod_volumes,
    get_shm_volumes
)
from schemas.tasks import TaskType


class ExperimentSpawner(K8SManager):
    MASTER_SERVICE = False

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
                 persist=False,
                 token_scope=None):
        self.spec = spec
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.original_name = original_name
        self.cloning_strategy = cloning_strategy
        self.persistence_config = persistence_config
        self.outputs_refs_experiments = outputs_refs_experiments
        self.outputs_refs_jobs = outputs_refs_jobs
        self.pod_manager = pods.PodManager(
            namespace=namespace,
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
            sidecar_config=sidecar_config,
            log_level=self.spec.log_level,
            original_name=self.original_name,
            cloning_strategy=self.cloning_strategy,
            declarations=self.spec.declarations,
            health_check_url=get_experiment_health_url(self.experiment_name))
        self.persist = persist
        self.token_scope = token_scope

        super().__init__(k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster)

        # Set the cluster_def
        cluster_def = self.get_cluster()
        self.pod_manager.set_cluster_def(cluster_def=cluster_def)

    def get_env_vars(self, task_type, task_idx):
        return None

    def get_resources(self, task_type, task_idx):
        return self.spec.master_resources

    def get_node_selector(self, task_type, task_idx):
        return self.spec.master_node_selector

    def get_affinity(self, task_type, task_idx):
        return self.spec.master_affinity

    def get_tolerations(self, task_type, task_idx):
        return self.spec.master_tolerations

    def get_n_pods(self, task_type):
        return 0

    def _create_job(self,
                    task_type,
                    task_idx,
                    add_service,
                    command=None,
                    args=None,
                    env_vars=None,
                    resources=None,
                    node_selector=None,
                    affinity=None,
                    tolerations=None,
                    restart_policy='Never'):
        ephemeral_token = RedisEphemeralTokens.generate_header_token(scope=self.token_scope)
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        sidecar_args = get_sidecar_args(pod_id=job_name,
                                        container_id=self.pod_manager.job_container_name,
                                        app_label=self.pod_manager.app_label)
        labels = self.pod_manager.get_labels(task_type=task_type, task_idx=task_idx)

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

        # Validate secret and configmap refs
        secret_refs = validate_secret_refs(self.spec.secret_refs)
        configmap_refs = validate_configmap_refs(self.spec.configmap_refs)

        pod = self.pod_manager.get_pod(
            task_type=task_type,
            task_idx=task_idx,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=labels,
            env_vars=env_vars,
            command=command,
            args=args,
            sidecar_args=sidecar_args,
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
            restart_policy=restart_policy)
        pod_resp, _ = self.create_or_update_pod(name=job_name, data=pod)
        results = {'pod': pod_resp.to_dict()}
        if add_service:
            service = services.get_service(namespace=self.namespace,
                                           name=job_name,
                                           labels=labels,
                                           ports=self.pod_manager.ports,
                                           target_ports=self.pod_manager.ports)
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
            node_selector = self.get_node_selector(task_type=task_type, task_idx=i)
            affinity = self.get_affinity(task_type=task_type, task_idx=i)
            tolerations = self.get_tolerations(task_type=task_type, task_idx=i)
            resp.append(self._create_job(task_type=task_type,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         env_vars=env_vars,
                                         resources=resources,
                                         node_selector=node_selector,
                                         affinity=affinity,
                                         tolerations=tolerations,
                                         add_service=add_service))
        return resp

    def _delete_job(self, task_type, task_idx, has_service):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        self.delete_pod(name=job_name, reraise=True)
        if has_service:
            self.delete_service(name=job_name, reraise=True)

    def delete_multi_jobs(self, task_type, has_service):
        n_pods = self.get_n_pods(task_type=task_type)
        deleted = True
        for i in range(n_pods):
            try:
                self._delete_job(task_type=task_type, task_idx=i, has_service=has_service)
            except PolyaxonK8SError:
                deleted = False
        return deleted

    def get_pod_command_args(self, task_type, task_idx):
        return get_pod_command_args(run_config=self.spec.run)

    def create_master(self):
        command, args = self.get_pod_command_args(task_type=TaskType.MASTER, task_idx=0)
        env_vars = self.get_env_vars(task_type=TaskType.MASTER, task_idx=0)
        resources = self.get_resources(task_type=TaskType.MASTER, task_idx=0)
        node_selector = self.get_node_selector(task_type=TaskType.MASTER, task_idx=0)
        affinity = self.get_affinity(task_type=TaskType.MASTER, task_idx=0)
        tolerations = self.get_tolerations(task_type=TaskType.MASTER, task_idx=0)
        return self._create_job(task_type=TaskType.MASTER,
                                task_idx=0,
                                command=command,
                                args=args,
                                env_vars=env_vars,
                                resources=resources,
                                node_selector=node_selector,
                                affinity=affinity,
                                tolerations=tolerations,
                                add_service=self.MASTER_SERVICE)

    def delete_master(self):
        try:
            self._delete_job(task_type=TaskType.MASTER, task_idx=0, has_service=self.MASTER_SERVICE)
            return True
        except PolyaxonK8SError:
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
            declarations=self.spec.declarations,
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
        return '{}:{}'.format(host, self.pod_manager.ports[0])

    def get_cluster(self):
        job_name = self.pod_manager.get_job_name(task_type=TaskType.MASTER, task_idx=0)
        return {
            TaskType.MASTER: [self._get_pod_address(job_name)]
        }
