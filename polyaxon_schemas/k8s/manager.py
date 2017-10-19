# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from kubernetes import client, config

from polyaxon_schemas.k8s.templates import config_maps
from polyaxon_schemas.k8s.templates import constants
from polyaxon_schemas.k8s.templates import deployments
from polyaxon_schemas.k8s.templates import persistent_volumes
from polyaxon_schemas.k8s.templates import pods
from polyaxon_schemas.k8s.templates import services
from polyaxon_schemas.utils import TaskType


class K8SManager(object):
    def __init__(self, polyaxonfile):
        self.polyaxonfile = polyaxonfile
        config.load_kube_config()
        self.k8s = client.CoreV1Api()
        self.k8s_beta = client.ExtensionsV1beta1Api()
        self.namespace = 'default'

        self.has_data_volume = False
        self.has_logs_volume = False
        self.has_files_volume = False
        self.has_tmp_volume = False

    def create_master(self, experiment=0):
        task_name = constants.TASK_NAME.format(project=self.polyaxonfile.project.name,
                                               experiment=experiment,
                                               task_type=TaskType.MASTER,
                                               task_id=0)
        labels = pods.get_labels(project=self.polyaxonfile.project.name,
                                 experiment=experiment,
                                 task_type=TaskType.MASTER,
                                 task_id=0,
                                 task_name=task_name)
        ports = [constants.DEFAULT_PORT]

        volumes, volume_mounts = self.get_pod_volumes()
        pod = pods.get_pod(project=self.polyaxonfile.project.name,
                           experiment=experiment,
                           task_type=TaskType.MASTER,
                           task_id=0,
                           volume_mounts=volume_mounts,
                           volumes=volumes,
                           ports=ports)
        self.k8s.create_namespaced_pod(self.namespace, pod)
        service = services.get_service(
            name=task_name,
            labels=labels,
            ports=ports)
        self.k8s.create_namespaced_service(self.namespace, service)

    def create_worker(self, experiment=0):
        n_pods = self.polyaxonfile.get_cluster_def_at(experiment)[0].get(TaskType.WORKER, 0)
        ports = [constants.DEFAULT_PORT]
        volumes, volume_mounts = self.get_pod_volumes()

        for i in range(n_pods):
            task_name = constants.TASK_NAME.format(project=self.polyaxonfile.project.name,
                                                   experiment=experiment,
                                                   task_type=TaskType.MASTER,
                                                   task_id=0)
            labels = pods.get_labels(project=self.polyaxonfile.project.name,
                                     experiment=experiment,
                                     task_type=TaskType.MASTER,
                                     task_id=0,
                                     task_name=task_name)
            pod = pods.get_pod(project=self.polyaxonfile.project.name,
                               experiment=experiment,
                               task_type=TaskType.WORKER,
                               task_id=i,
                               volume_mounts=volume_mounts,
                               volumes=volumes,
                               ports=ports)
            self.k8s.create_namespaced_pod(self.namespace, pod)
            service = services.get_service(
                name=task_name,
                labels=labels,
                ports=ports)
            self.k8s.create_namespaced_service(self.namespace, service)

    def create_ps(self, experiment=0):
        n_pods = self.polyaxonfile.get_cluster_def_at(experiment)[0].get(TaskType.PS, 0)
        volumes, volume_mounts = self.get_pod_volumes()
        ports = [constants.DEFAULT_PORT]

        for i in range(n_pods):
            task_name = constants.TASK_NAME.format(project=self.polyaxonfile.project.name,
                                                   experiment=experiment,
                                                   task_type=TaskType.MASTER,
                                                   task_id=0)
            labels = pods.get_labels(project=self.polyaxonfile.project.name,
                                     experiment=experiment,
                                     task_type=TaskType.MASTER,
                                     task_id=0,
                                     task_name=task_name)
            pod = pods.get_pod(project=self.polyaxonfile.project.name,
                               experiment=experiment,
                               task_type=TaskType.PS,
                               task_id=i,
                               volume_mounts=volume_mounts,
                               volumes=volumes,
                               ports=ports)
            self.k8s.create_namespaced_pod(self.namespace, pod)
            service = services.get_service(
                name=task_name,
                labels=labels,
                ports=ports)
            self.k8s.create_namespaced_service(self.namespace, service)

    def create_tensorboard_deployment(self):
        name = 'tensorboard'
        ports = [6006]
        volumes, volume_mounts = self.get_pod_volumes()
        logs_path = os.path.join('/', constants.LOGS_VOLUME)
        deployment = deployments.get_deployment(name=name,
                                                project=self.polyaxonfile.project.name,
                                                volume_mounts=volume_mounts,
                                                volumes=volumes,
                                                args=['tensorboard --logdir={} --port=6006'.format(
                                                    logs_path)],
                                                ports=ports,
                                                role='dashboard')
        self.k8s_beta.create_namespaced_deployment(self.namespace, deployment)
        service = services.get_service(
            name=name,
            labels=deployments.get_labels(name=name,
                                          project=self.polyaxonfile.project.name,
                                          role='dashboard'),
            ports=ports,
            service_type='LoadBalancer')
        self.k8s.create_namespaced_service(self.namespace, service)

    def get_pod_volumes(self):
        volumes = []
        volume_mounts = []
        if self.has_data_volume:
            volumes.append(pods.get_volume(volume=constants.DATA_VOLUME,
                                           run_type=self.polyaxonfile.run_type))
            volume_mounts.append(pods.get_volume_mount(constants.DATA_VOLUME))

        if self.has_logs_volume:
            volumes.append(pods.get_volume(volume=constants.LOGS_VOLUME,
                                           run_type=self.polyaxonfile.run_type))
            volume_mounts.append(pods.get_volume_mount(constants.LOGS_VOLUME))

        if self.has_files_volume:
            volumes.append(pods.get_volume(volume=constants.POLYAXON_FILES_VOLUME,
                                           run_type=self.polyaxonfile.run_type))
            volume_mounts.append(pods.get_volume_mount(constants.POLYAXON_FILES_VOLUME))

        if self.has_tmp_volume:
            volumes.append(pods.get_volume(volume=constants.TMP_VOLUME,
                                           run_type=self.polyaxonfile.run_type))
            volume_mounts.append(pods.get_volume_mount(constants.TMP_VOLUME))

        return volumes, volume_mounts

    def _create_volume(self, volume):
        pvol = persistent_volumes.get_persistent_volume(volume=volume,
                                                        run_type=self.polyaxonfile.run_type)
        self.k8s.create_persistent_volume(pvol)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(volume=volume)
        self.k8s.create_namespaced_persistent_volume_claim(self.namespace, pvol_claim)

    def create_data_volume(self):
        self._create_volume(constants.DATA_VOLUME)
        self.has_data_volume = True

    def create_logs_volume(self):
        self._create_volume(constants.LOGS_VOLUME)
        self.has_logs_volume = True

    def create_tmp_volumes(self):
        self._create_volume(constants.TMP_VOLUME)
        self.has_tmp_volume = True

    def create_files_volumes(self):
        self._create_volume(constants.POLYAXON_FILES_VOLUME)
        self.has_files_volume = True

    def _delete_volume(self, volume):
        self.k8s.delete_persistent_volume(
            volume,
            client.V1DeleteOptions(api_version=constants.K8S_API_VERSION_V1))
        self.k8s.delete_namespaced_persistent_volume_claim(
            volume,
            self.namespace,
            client.V1DeleteOptions(api_version=constants.K8S_API_VERSION_V1))

    def delete_data_volume(self):
        self._delete_volume(constants.DATA_VOLUME)
        self.has_data_volume = False

    def delete_logs_volume(self):
        self._delete_volume(constants.LOGS_VOLUME)
        self.has_logs_volume = False

    def delete_tmp_volumes(self):
        self._create_volume(constants.TMP_VOLUME)
        self.has_tmp_volume = True

    def delete_files_volumes(self):
        self._delete_volume(constants.POLYAXON_FILES_VOLUME)
        self.has_files_volume = False

    def delete_volumes(self):
        self.delete_data_volume()
        self.delete_logs_volume()
        self.delete_files_volumes()
        self.delete_tmp_volumes()

    def create_volumes(self):
        self.create_data_volume()
        self.create_logs_volume()
        self.create_files_volumes()
        self.create_tmp_volumes()

    def create_cluster_config_map(self, experiment=0):
        config_map = config_maps.get_cluster_config_map(
            project=self.polyaxonfile.project.name,
            experiment=experiment,
            cluster_def=self.polyaxonfile.get_cluster().to_dict())
        self.k8s.create_namespaced_config_map(self.namespace, config_map)
