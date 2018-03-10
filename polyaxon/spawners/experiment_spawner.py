# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import logging

from kubernetes import client
from kubernetes.client.rest import ApiException

from polyaxon_k8s import constants as k8s_constants
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager

from polyaxon_schemas.polyaxonfile.specification import Specification
from polyaxon_schemas.environments import ClusterConfig
from polyaxon_schemas.utils import TaskType

from spawners.base import get_pod_volumes
from spawners.templates import config_maps
from spawners.templates import constants
from spawners.templates import persistent_volumes
from spawners.templates import pods
from spawners.templates import services

logger = logging.getLogger('polyaxon.spawners.spawners')


class ExperimentSpawner(K8SManager):
    def __init__(self,
                 project_name,
                 experiment_name,
                 project_uuid,
                 experiment_uuid,
                 spec_config,
                 experiment_group_uuid=None,
                 experiment_group_name=None,
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
                 sidecar_args_fn=None,
                 persist=False):
        self.spec = Specification.read(spec_config)
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.pod_manager = pods.PodManager(namespace=namespace,
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
                                           sidecar_config=sidecar_config)
        self.sidecar_args_fn = sidecar_args_fn or constants.SIDECAR_ARGS_FN
        self.persist = persist

        super(ExperimentSpawner, self).__init__(k8s_config=k8s_config,
                                                namespace=namespace,
                                                in_cluster=in_cluster)

    def _create_pod(self,
                    task_type,
                    task_idx,
                    command=None,
                    args=None,
                    sidecar_args_fn=None,
                    resources=None,
                    restart_policy='Never'):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        sidecar_args = sidecar_args_fn(pod_id=job_name)
        labels = self.pod_manager.get_labels(task_type=task_type, task_idx=task_idx)

        volumes, volume_mounts = get_pod_volumes()
        pod = self.pod_manager.get_pod(task_type=task_type,
                                       task_idx=task_idx,
                                       volume_mounts=volume_mounts,
                                       volumes=volumes,
                                       command=command,
                                       args=args,
                                       sidecar_args=sidecar_args,
                                       resources=resources,
                                       restart_policy=restart_policy)
        pod_resp, _ = self.create_or_update_pod(name=job_name, data=pod)

        service = services.get_service(namespace=self.namespace,
                                       name=job_name,
                                       labels=labels,
                                       ports=self.pod_manager.ports,
                                       target_ports=self.pod_manager.ports)
        service_resp, _ = self.create_or_update_service(name=job_name, data=service)
        return {
            'pod': pod_resp.to_dict(),
            'service': service_resp.to_dict()
        }

    def _delete_pod(self, task_type, task_idx):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        self.delete_pod(name=job_name)
        self.delete_service(name=job_name)

    def create_master(self, resources=None):
        command, args = self.get_pod_cmd_args(task_type=TaskType.MASTER,
                                              task_idx=0,
                                              schedule='train_and_evaluate')
        return self._create_pod(task_type=TaskType.MASTER,
                                task_idx=0,
                                command=command,
                                args=args,
                                sidecar_args_fn=self.sidecar_args_fn,
                                resources=resources)

    def delete_master(self):
        self._delete_pod(task_type=TaskType.MASTER, task_idx=0)

    def _create_worker(self, resources, n_pods):
        resp = []
        for i in range(n_pods):
            command, args = self.get_pod_cmd_args(task_type=TaskType.WORKER,
                                                  task_idx=i,
                                                  schedule='train')
            resp.append(self._create_pod(task_type=TaskType.WORKER,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         sidecar_args_fn=self.sidecar_args_fn,
                                         resources=resources.get(i)))
        return resp

    def _delete_worker(self, n_pods):
        for i in range(n_pods):
            self._delete_pod(task_type=TaskType.WORKER, task_idx=i)

    def _create_ps(self, resources, n_pods):
        resp = []
        for i in range(n_pods):
            command, args = self.get_pod_cmd_args(task_type=TaskType.PS,
                                                  task_idx=i,
                                                  schedule='run_std_server')
            resp.append(self._create_pod(task_type=TaskType.PS,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         sidecar_args_fn=self.sidecar_args_fn,
                                         resources=resources.get(i)))
        return resp

    def _delete_ps(self, n_pods):
        for i in range(n_pods):
            self._delete_pod(task_type=TaskType.PS, task_idx=i)

    def has_volume(self, volume):
        persistent_volume = self.get_volume(volume)
        volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
        volume_claime = self.get_volume_claim(volc_name)
        return persistent_volume is not None and volume_claime is not None

    def check_data_volume(self):
        if not self.has_volume(constants.DATA_VOLUME):
            logger.warning('Unable to find a data volume to mount to job.')

    def check_outputs_volume(self):
        if not self.has_volume(constants.OUTPUTS_VOLUME):
            logger.warning('Unable to find a outputs volume to mount to job.')

    def _create_volume(self, volume):
        pvol = persistent_volumes.get_persistent_volume(namespace=self.namespace,
                                                        volume=volume,
                                                        run_type=self.spec.run_type)

        self.create_or_update_volume(name=volume, data=pvol)

        volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(namespace=self.namespace,
                                                                    volume=volume)

        self.create_or_update_volume_claim(name=volc_name, data=pvol_claim)

    def _delete_volume(self, volume):
        volume_found = False
        try:
            self.k8s_api.read_persistent_volume(volume)
            volume_found = True
            self.k8s_api.delete_persistent_volume(
                volume,
                client.V1DeleteOptions(api_version=k8s_constants.K8S_API_VERSION_V1))
            logger.debug('Volume `{}` Deleted'.format(volume))
        except ApiException as e:
            if volume_found:
                logger.warning('Could not delete volume `{}`'.format(volume))
                raise PolyaxonK8SError(e)
            else:
                logger.debug('Volume `{}` was not found'.format(volume))

        volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
        volume_claim_found = False
        try:
            self.k8s_api.read_namespaced_persistent_volume_claim(volc_name, self.namespace)
            volume_claim_found = True
            self.k8s_api.delete_namespaced_persistent_volume_claim(
                volc_name,
                self.namespace,
                client.V1DeleteOptions(api_version=k8s_constants.K8S_API_VERSION_V1))
            logger.debug('Volume claim `{}` Deleted'.format(volc_name))
        except ApiException as e:
            if volume_claim_found:
                logger.warning('Could not delete volume claim `{}`'.format(volc_name))
                raise PolyaxonK8SError(e)
            else:
                logger.debug('Volume claim `{}` was not found'.format(volc_name))

    def create_experiment_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(experiment_uuid=self.experiment_uuid)
        config_map = config_maps.get_config_map(
            namespace=self.namespace,
            project_name=self.project_name,
            experiment_group_name=self.experiment_group_name,
            experiment_name=self.experiment_name,
            project_uuid=self.project_uuid,
            experiment_group_uuid=self.experiment_group_uuid,
            experiment_uuid=self.experiment_uuid,
            cluster_def=self.get_cluster().to_dict(),
            declarations=self.spec.declarations,
            log_level=self.spec.log_level
        )

        self.create_or_update_config_map(name=name, body=config_map, reraise=True)

    def create_experiment_secret(self, user_token):
        name = constants.SECRET_NAME.format(experiment_uuid=self.experiment_uuid)
        secret = config_maps.get_secret(
            namespace=self.namespace,
            project_name=self.project_name,
            experiment_group_name=self.experiment_group_name,
            experiment_name=self.experiment_name,
            project_uuid=self.project_uuid,
            experiment_group_uuid=self.experiment_group_uuid,
            experiment_uuid=self.experiment_uuid,
            user_token=user_token
        )

        self.create_or_update_secret(name=name, body=secret, reraise=True)

    def delete_experiment_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(experiment_uuid=self.experiment_uuid)
        self.delete_config_map(name, reraise=True)

    def delete_experiment_secret(self):
        name = constants.SECRET_NAME.format(experiment_uuid=self.experiment_uuid)
        self.delete_secret(name, reraise=True)

    def get_pod_cmd_args(self, task_type, task_idx, schedule):
        if self.spec.run_exec:
            cmd = self.spec.run_exec.cmd.split(' ')
            cmd = [c.strip().strip('\\') for c in cmd if (c and c != '\\')]
            cmd = [c for c in cmd if (c and c != '\\')]
            return cmd, []

        spec_data = json.dumps(self.spec.parsed_data)

        args = [
            "from polyaxon.polyaxonfile.local_runner import start_experiment_run; "
            "start_experiment_run('{polyaxonfile}', '{experiment_id}', "
            "'{task_type}', {task_idx}, '{schedule}')".format(
                polyaxonfile=spec_data,
                experiment_id=0,
                task_type=task_type,
                task_idx=task_idx,
                schedule=schedule)]
        return ["python3", "-c"], args

    def create_worker(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)
        resources = self.spec.worker_resources
        return self._create_worker(resources=resources, n_pods=n_pods)

    def delete_worker(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)
        self._delete_worker(n_pods=n_pods)

    def create_ps(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.PS, 0)
        resources = self.spec.ps_resources
        return self._create_ps(resources=resources, n_pods=n_pods)

    def delete_ps(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.PS, 0)
        self._delete_ps(n_pods=n_pods)

    def start_experiment(self, user_token=None):
        self.check_data_volume()
        self.check_outputs_volume()
        self.create_experiment_config_map()
        self.create_experiment_secret(user_token)
        master_resp = self.create_master(resources=self.spec.master_resources)
        worker_resp = self.create_worker()
        ps_resp = self.create_ps()
        return {
            TaskType.MASTER: master_resp,
            TaskType.WORKER: worker_resp,
            TaskType.PS: ps_resp
        }

    def stop_experiment(self):
        self.delete_experiment_config_map()
        self.delete_experiment_secret()
        self.delete_master()
        self.delete_worker()
        self.delete_ps()

    def get_task_phase(self, task_type, task_idx):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        return self.k8s_api.read_namespaced_pod_status(job_name, self.namespace).status.phase

    def get_task_log(self, task_type, task_idx, **kwargs):
        job_name = self.pod_manager.get_job_name(task_type=task_type, task_idx=task_idx)
        return self.k8s_api.read_namespaced_pod_log(job_name, self.namespace, **kwargs)

    def get_experiment_phase(self):
        return self.get_task_phase(task_type=TaskType.MASTER, task_idx=0)

    def get_cluster(self, port=constants.DEFAULT_PORT):
        cluster_def, is_distributed = self.spec.cluster_def

        def get_address(host):
            return '{}:{}'.format(host, port)

        job_name = self.pod_manager.get_job_name(task_type=TaskType.MASTER, task_idx=0)
        cluster_config = {
            TaskType.MASTER: [get_address(job_name)]
        }

        workers = []
        for i in range(cluster_def.get(TaskType.WORKER, 0)):
            job_name = self.pod_manager.get_job_name(task_type=TaskType.WORKER, task_idx=i)
            workers.append(get_address(job_name))

        cluster_config[TaskType.WORKER] = workers

        ps = []
        for i in range(cluster_def.get(TaskType.PS, 0)):
            job_name = self.pod_manager.get_job_name(task_type=TaskType.PS, task_idx=i)
            ps.append(get_address(job_name))

        cluster_config[TaskType.PS] = ps

        return ClusterConfig.from_dict(cluster_config)
