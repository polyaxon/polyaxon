# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from polyaxon_schemas.exceptions import PolyaxonK8SError
from polyaxon_schemas.polyaxonfile.logger import logger
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

    def _create_pod(self, experiment, task_type, task_id):
        task_name = constants.TASK_NAME.format(project=self.polyaxonfile.project.name,
                                               experiment=experiment,
                                               task_type=task_type,
                                               task_id=task_id)
        labels = pods.get_labels(project=self.polyaxonfile.project.name,
                                 experiment=experiment,
                                 task_type=task_type,
                                 task_id=task_id,
                                 task_name=task_name)
        ports = [constants.DEFAULT_PORT]

        volumes, volume_mounts = self.get_pod_volumes()
        pod = pods.get_pod(project=self.polyaxonfile.project.name,
                           experiment=experiment,
                           task_type=task_type,
                           task_id=task_id,
                           volume_mounts=volume_mounts,
                           volumes=volumes,
                           ports=ports)

        pod_found = False
        try:
            self.k8s.read_namespaced_pod(task_name, self.namespace)
            pod_found = True
            logger.info('A pod with name `{}` was found'.format(task_name))
            self.k8s.patch_namespaced_pod(task_name, self.namespace, pod)
            logger.info('Pod `{}` was patched'.format(task_name))
        except ApiException as e:
            if pod_found:
                raise PolyaxonK8SError(e)
            self.k8s.create_namespaced_pod(self.namespace, pod)
            logger.info('Pod `{}` was created'.format(task_name))

        service = services.get_service(name=task_name, labels=labels, ports=ports)

        service_found = False
        try:
            self.k8s.read_namespaced_service(task_name, self.namespace)
            service_found = True
            logger.info('A service with name `{}` was found'.format(task_name))
            self.k8s.patch_namespaced_pod(task_name, self.namespace, service)
            logger.info('Service `{}` was patched'.format(task_name))
        except ApiException as e:
            if service_found:
                raise PolyaxonK8SError(e)
            self.k8s.create_namespaced_service(self.namespace, service)
            logger.info('Service `{}` was created'.format(task_name))

    def _delete_pod(self, experiment, task_type, task_id):
        task_name = constants.TASK_NAME.format(project=self.polyaxonfile.project.name,
                                               experiment=experiment,
                                               task_type=task_type,
                                               task_id=task_id)
        pod_found = False
        try:
            self.k8s.read_namespaced_pod(task_name, self.namespace)
            pod_found = True
            self.k8s.delete_namespaced_pod(
                task_name,
                self.namespace,
                client.V1DeleteOptions(api_version=constants.K8S_API_VERSION_V1))
            logger.info('Pod `{}` deleted'.format(task_name))
        except ApiException as e:
            if pod_found:
                logger.warning('Could not delete pod `{}`'.format(task_name))
                raise PolyaxonK8SError(e)
            else:
                logger.info('Pod `{}` was not found'.format(task_name))

        service_found = False
        try:
            self.k8s.read_namespaced_service(task_name, self.namespace)
            service_found = True
            self.k8s.delete_namespaced_service(
                task_name,
                self.namespace)
            logger.info('Service `{}` deleted'.format(task_name))
        except ApiException as e:
            if service_found:
                logger.warning('Could not delete service `{}`'.format(task_name))
                raise PolyaxonK8SError(e)
            else:
                logger.info('Service `{}` was not found'.format(task_name))

    def create_master(self, experiment=0):
        self._create_pod(experiment=experiment, task_type=TaskType.MASTER, task_id=0)

    def delete_master(self, experiment=0):
        self._delete_pod(experiment=experiment, task_type=TaskType.MASTER, task_id=0)

    def create_worker(self, experiment=0):
        n_pods = self.polyaxonfile.get_cluster_def_at(experiment)[0].get(TaskType.WORKER, 0)
        for i in range(n_pods):
            self._create_pod(experiment=experiment, task_type=TaskType.WORKER, task_id=i)

    def delete_worker(self, experiment=0):
        n_pods = self.polyaxonfile.get_cluster_def_at(experiment)[0].get(TaskType.WORKER, 0)
        for i in range(n_pods):
            self._delete_pod(experiment=experiment, task_type=TaskType.WORKER, task_id=i)

    def create_ps(self, experiment=0):
        n_pods = self.polyaxonfile.get_cluster_def_at(experiment)[0].get(TaskType.PS, 0)
        for i in range(n_pods):
            self._create_pod(experiment=experiment, task_type=TaskType.PS, task_id=i)

    def delete_ps(self, experiment=0):
        n_pods = self.polyaxonfile.get_cluster_def_at(experiment)[0].get(TaskType.PS, 0)
        for i in range(n_pods):
            self._delete_pod(experiment=experiment, task_type=TaskType.PS, task_id=i)

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
            volumes.append(pods.get_volume(volume=constants.DATA_VOLUME))
            volume_mounts.append(pods.get_volume_mount(constants.DATA_VOLUME))

        if self.has_logs_volume:
            volumes.append(pods.get_volume(volume=constants.LOGS_VOLUME))
            volume_mounts.append(pods.get_volume_mount(constants.LOGS_VOLUME))

        if self.has_files_volume:
            volumes.append(pods.get_volume(volume=constants.POLYAXON_FILES_VOLUME))
            volume_mounts.append(pods.get_volume_mount(constants.POLYAXON_FILES_VOLUME))

        if self.has_tmp_volume:
            volumes.append(pods.get_volume(volume=constants.TMP_VOLUME))
            volume_mounts.append(pods.get_volume_mount(constants.TMP_VOLUME))

        return volumes, volume_mounts

    def _create_volume(self, volume):
        volume_name = constants.VOLUME_NAME.format(vol_name=volume)
        pvol = persistent_volumes.get_persistent_volume(volume=volume,
                                                        run_type=self.polyaxonfile.run_type)

        volume_found = False
        try:
            self.k8s.read_persistent_volume(volume_name)
            volume_found = True
            logger.info('A volume with name `{}` was found'.format(volume_name))
            self.k8s.patch_persistent_volume(volume_name, pvol)
            logger.info('Volume `{}` was patched'.format(volume_name))
        except ApiException as e:
            if volume_found:
                raise PolyaxonK8SError(e)
            self.k8s.create_persistent_volume(pvol)
            logger.info('Volume `{}` was created'.format(volume_name))

        pvol_claim = persistent_volumes.get_persistent_volume_claim(volume=volume)
        volume_claim_found = False
        try:
            self.k8s.read_namespaced_persistent_volume_claim(volume_name, self.namespace)
            volume_claim_found = True
            logger.info('A volume claim with name `{}` was found'.format(volume_name))
            self.k8s.patch_namespaced_persistent_volume_claim(volume_name,
                                                              self.namespace,
                                                              pvol_claim)
            logger.info('Volume claim `{}` was patched'.format(volume_name))
        except ApiException:
            if volume_claim_found:
                raise PolyaxonK8SError(e)
            self.k8s.create_namespaced_persistent_volume_claim(self.namespace, pvol_claim)
            logger.info('Volume claim `{}` was created'.format(volume_name))

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
        volume_name = constants.VOLUME_NAME.format(vol_name=volume)
        volume_found = False
        try:
            self.k8s.read_persistent_volume(volume_name)
            volume_found = True
            self.k8s.delete_persistent_volume(
                volume_name,
                client.V1DeleteOptions(api_version=constants.K8S_API_VERSION_V1))
            logger.info('Volume `{}` Deleted'.format(volume_name))
        except ApiException as e:
            if volume_found:
                logger.warning('Could not delete volume `{}`'.format(volume_name))
                raise PolyaxonK8SError(e)
            else:
                logger.info('Volume `{}` was not found'.format(volume_name))

        volume_claim_found = False
        try:
            self.k8s.read_namespaced_persistent_volume_claim(volume_name, self.namespace)
            volume_claim_found = True
            self.k8s.delete_namespaced_persistent_volume_claim(
                volume_name,
                self.namespace,
                client.V1DeleteOptions(api_version=constants.K8S_API_VERSION_V1))
            logger.info('Volume claim `{}` Deleted'.format(volume_name))
        except ApiException as e:
            if volume_claim_found:
                logger.warning('Could not delete volume claim `{}`'.format(volume_name))
                raise PolyaxonK8SError(e)
            else:
                logger.info('Volume claim `{}` was not found'.format(volume_name))

    def delete_data_volume(self):
        self._delete_volume(constants.DATA_VOLUME)
        self.has_data_volume = False

    def delete_logs_volume(self):
        self._delete_volume(constants.LOGS_VOLUME)
        self.has_logs_volume = False

    def delete_tmp_volumes(self):
        self._delete_volume(constants.TMP_VOLUME)
        self.has_tmp_volume = False

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
        name = constants.CONFIG_MAP_CLUSTER_NAME.format(project=self.polyaxonfile.project.name,
                                                        experiment=experiment)
        config_map = config_maps.get_cluster_config_map(
            project=self.polyaxonfile.project.name,
            experiment=experiment,
            cluster_def=self.polyaxonfile.get_cluster().to_dict())

        config_map_found = False
        try:
            self.k8s.read_namespaced_config_map(name, self.namespace)
            config_map_found = True
            logger.info('A config map with name `{}` was found'.format(name))
            self.k8s.patch_namespaced_config_map(name, self.namespace, config_map)
            logger.info('Config map `{}` was patched'.format(name))
        except ApiException as e:
            if config_map_found:
                raise PolyaxonK8SError(e)
            self.k8s.create_namespaced_config_map(self.namespace, config_map)
            logger.info('Config map `{}` was created'.format(name))

    def delete_cluster_config_map(self, experiment=0):
        name = constants.CONFIG_MAP_CLUSTER_NAME.format(project=self.polyaxonfile.project.name,
                                                        experiment=experiment)

        config_map_found = False
        try:
            self.k8s.read_namespaced_config_map(name, self.namespace)
            config_map_found = True
            self.k8s.delete_namespaced_config_map(
                name,
                self.namespace,
                client.V1DeleteOptions(api_version=constants.K8S_API_VERSION_V1))
            logger.info('Config map `{}` Deleted'.format(name))
        except ApiException as e:
            if config_map_found:
                logger.warning('Could not delete config map `{}`'.format(name))
                raise PolyaxonK8SError(e)
            else:
                logger.info('Config map `{}` was not found'.format(name))

    def create_experiment(self, experiment=0):
        self.create_cluster_config_map(experiment)
        self.create_volumes()
        self.create_master(experiment)
        self.create_worker(experiment)
        self.create_ps(experiment)

    def delete_experiment(self, experiment=0):
        self.delete_cluster_config_map(experiment)
        self.delete_volumes()
        self.delete_master(experiment)
        self.delete_worker(experiment)
        self.delete_ps(experiment)
