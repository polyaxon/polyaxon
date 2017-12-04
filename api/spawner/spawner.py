# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import logging

from kubernetes import client
from kubernetes.client.rest import ApiException

from polyaxon_k8s import constants as k8s_constants
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager

from polyaxon_schemas.polyaxonfile.polyaxonfile import Specification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import TaskType

from spawner.templates import config_maps
from spawner.templates import constants
from spawner.templates import deployments
from spawner.templates import persistent_volumes
from spawner.templates import pods
from spawner.templates import services

logger = logging.getLogger('polyaxon.tasks.projects')


class K8SSpawner(K8SManager):
    def __init__(self,
                 project_uuid,
                 experiment_uuid,
                 spec_config,
                 spec_uuid=None,
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
                 sidecar_args_fn=None):
        self.specification = Specification.read(spec_config)
        self.project_uuid = project_uuid
        self.spec_uuid = spec_uuid
        self.experiment_uuid = experiment_uuid
        self.has_data_volume = False
        self.has_logs_volume = False
        self.pod_manager = pods.PodManager(namespace=namespace,
                                           project=self.project_name,
                                           experiment=experiment_uuid,
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

        super(K8SSpawner, self).__init__(k8s_config=k8s_config,
                                         namespace=namespace,
                                         in_cluster=in_cluster)

    @property
    def spec(self):
        return self.specification

    @cached_property
    def project_name(self):
        return self.spec.project.name.replace('_', '-')

    def _create_pod(self,
                    task_type,
                    task_idx,
                    command=None,
                    args=None,
                    sidecar_args_fn=None,
                    resources=None,
                    restart_policy='Never'):
        task_name = self.pod_manager.get_task_name(task_type=task_type, task_idx=task_idx)
        sidecar_args = sidecar_args_fn(container_job_name=self.pod_manager.job_container_name,
                                       pod_id=task_name)
        labels = self.pod_manager.get_labels(task_type=task_type,
                                             task_idx=task_idx,
                                             task_name=task_name)

        volumes, volume_mounts = self.get_pod_volumes()
        pod = self.pod_manager.get_pod(task_type=task_type,
                                       task_idx=task_idx,
                                       volume_mounts=volume_mounts,
                                       volumes=volumes,
                                       command=command,
                                       args=args,
                                       sidecar_args=sidecar_args,
                                       resources=resources,
                                       restart_policy=restart_policy)
        pod_resp, _ = self.create_or_update_pod(name=task_name, data=pod)

        service = services.get_service(namespace=self.namespace,
                                       name=task_name,
                                       labels=labels,
                                       ports=self.pod_manager.ports)
        service_resp, _ = self.create_or_update_service(name=task_name, data=service)
        return {
            'pod': pod_resp.to_dict(),
            'service': service_resp.to_dict()
        }

    def _delete_pod(self, task_type, task_idx):
        task_name = self.pod_manager.get_task_name(task_type=task_type, task_idx=task_idx)
        self.delete_pod(name=task_name)
        self.delete_service(name=task_name)

    def create_master(self, resources=None):
        args = self.get_pod_args(task_type=TaskType.MASTER,
                                 task_idx=0,
                                 schedule='train_and_evaluate')
        command = ["python3", "-c"]
        return self._create_pod(task_type=TaskType.MASTER,
                                task_idx=0,
                                command=command,
                                args=args,
                                sidecar_args_fn=self.sidecar_args_fn,
                                resources=resources)

    def delete_master(self):
        self._delete_pod(task_type=TaskType.MASTER, task_idx=0)

    def _create_worker(self, resources, n_pods):
        command = ["python3", "-c"]
        resp = []
        for i in range(n_pods):
            args = self.get_pod_args(task_type=TaskType.WORKER,
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
        command = ["python3", "-c"]
        resp = []
        for i in range(n_pods):
            args = self.get_pod_args(task_type=TaskType.PS,
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

    def create_tensorboard_deployment(self):
        name = 'tensorboard'
        ports = [6006]
        volumes, volume_mounts = self.get_pod_volumes()
        logs_path = persistent_volumes.get_vol_path(volume=constants.LOGS_VOLUME,
                                                    run_type=self.spec.run_type)
        deployment = deployments.get_deployment(
            namespace=self.namespace,
            name=name,
            project=self.project_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            command=["/bin/sh", "-c"],
            args=["tensorboard --logdir={} --port=6006".format(logs_path)],
            ports=ports,
            role='dashboard')
        deployment_name = constants.DEPLOYMENT_NAME.format(project=self.project_name, name=name)

        self.create_or_update_deployment(name=deployment_name, data=deployment)
        service = services.get_service(
            namespace=self.namespace,
            name=deployment_name,
            labels=deployments.get_labels(name=name, project=self.project_name, role='dashboard'),
            ports=ports,
            service_type='LoadBalancer')

        self.create_or_update_service(name=deployment_name, data=service)

    def delete_tensorboard_deployment(self):
        name = 'tensorboard'
        deployment_name = constants.DEPLOYMENT_NAME.format(project=self.project_name, name=name)
        self.delete_deployment(name=deployment_name)
        self.delete_service(name=deployment_name)

    def get_pod_volumes(self):
        volumes = []
        volume_mounts = []
        if self.has_data_volume:
            volumes.append(pods.get_volume(volume=constants.DATA_VOLUME))
            volume_mounts.append(pods.get_volume_mount(volume=constants.DATA_VOLUME,
                                                       run_type=self.spec.run_type))

        if self.has_logs_volume:
            volumes.append(pods.get_volume(volume=constants.LOGS_VOLUME))
            volume_mounts.append(pods.get_volume_mount(volume=constants.LOGS_VOLUME,
                                                       run_type=self.spec.run_type))
        return volumes, volume_mounts

    def has_volume(self, volume):
        vol_name = constants.VOLUME_NAME.format(vol_name=volume)
        persistent_volume = self.get_volume(vol_name)
        volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
        volume_claime = self.get_volume_claim(volc_name)
        return persistent_volume is not None and volume_claime is not None

    def check_data_volume(self):
        self.has_data_volume = self.has_volume(constants.DATA_VOLUME)

    def check_logs_volume(self):
        self.has_data_volume = self.has_volume(constants.LOGS_VOLUME)

    def _create_volume(self, volume):
        vol_name = constants.VOLUME_NAME.format(vol_name=volume)
        pvol = persistent_volumes.get_persistent_volume(namespace=self.namespace,
                                                        volume=volume,
                                                        run_type=self.spec.run_type)

        self.create_or_update_volume(name=vol_name, data=pvol)

        volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(namespace=self.namespace,
                                                                    volume=volume)

        self.create_or_update_volume_claim(name=volc_name, data=pvol_claim)

    def _delete_volume(self, volume):
        vol_name = constants.VOLUME_NAME.format(vol_name=volume)
        volume_found = False
        try:
            self.k8s_api.read_persistent_volume(vol_name)
            volume_found = True
            self.k8s_api.delete_persistent_volume(
                vol_name,
                client.V1DeleteOptions(api_version=k8s_constants.K8S_API_VERSION_V1))
            logger.debug('Volume `{}` Deleted'.format(vol_name))
        except ApiException as e:
            if volume_found:
                logger.warning('Could not delete volume `{}`'.format(vol_name))
                raise PolyaxonK8SError(e)
            else:
                logger.debug('Volume `{}` was not found'.format(vol_name))

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

    def create_cluster_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(project=self.project_name,
                                                experiment=self.experiment_uuid,
                                                role='cluster')
        config_map = config_maps.get_cluster_config_map(
            namespace=self.namespace,
            project=self.project_name,
            experiment=self.experiment_uuid,
            cluster_def=self.spec.get_cluster().to_dict())

        self.create_or_update_config_map(name=name, body=config_map, reraise=True)

    def delete_cluster_config_map(self):
        name = constants.CONFIG_MAP_NAME.format(project=self.project_name,
                                                experiment=self.experiment_uuid,
                                                role='cluster')
        self.delete_config_map(name, reraise=True)

    @cached_property
    def project_name(self):
        if self.spec_uuid:
            return '{}-id{}-spec{}'.format(self.spec.project.name.replace('_', '-'),
                                           self.project_uuid,
                                           self.spec_uuid)
        else:
            return '{}-id{}'.format(self.spec.project.name.replace('_', '-'),
                                    self.project_uuid)

    def get_pod_args(self, task_type, task_idx, schedule):
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
        return args

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

    def start_experiment(self):
        self.check_data_volume()
        self.check_logs_volume()
        self.create_cluster_config_map()
        master_resp = self.create_master(resources=self.spec.master_resources)
        worker_resp = self.create_worker()
        ps_resp = self.create_ps()
        return {
            TaskType.MASTER: master_resp,
            TaskType.WORKER: worker_resp,
            TaskType.PS: ps_resp
        }

    def delete_experiment(self):
        self.delete_cluster_config_map()
        self.delete_master()
        self.delete_worker()
        self.delete_ps()

    def get_task_phase(self, task_type, task_idx):
        self.pod_manager.set_experiment(self.experiment_uuid)
        task_name = self.pod_manager.get_task_name(task_type=task_type, task_idx=task_idx)
        return self.k8s_api.read_namespaced_pod_status(task_name, self.namespace).status.phase

    def get_task_log(self, task_type, task_idx, **kwargs):
        self.pod_manager.set_experiment(self.experiment_uuid)
        task_name = self.pod_manager.get_task_name(task_type=task_type, task_idx=task_idx)
        return self.k8s_api.read_namespaced_pod_log(task_name, self.namespace, **kwargs)

    def get_experiment_phase(self):
        return self.get_task_phase(task_type=TaskType.MASTER, task_idx=0)
