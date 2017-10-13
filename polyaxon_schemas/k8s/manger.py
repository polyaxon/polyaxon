# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from kubernetes import client, config

from polyaxon_schemas.k8s.templates import config_maps
from polyaxon_schemas.k8s.templates import constants
from polyaxon_schemas.k8s.templates import persistent_volumes


class K8SManager(object):
    def __init__(self, polyaxonfile):
        self.polyaxonfile = polyaxonfile
        config.load_kube_config()
        self.k8s = client.CoreV1Api()
        self.namespace = 'default'

        self.has_data_volume = False
        self.has_logs_volume = False
        self.has_files_volume = False
        self.has_tmp_volume = False

    @classmethod
    def create_master(cls):
        pass

    @classmethod
    def create_worker(cls):
        pass

    @classmethod
    def create_ps(cls):
        pass

    @classmethod
    def config_maps(cls):
        pass

    @classmethod
    def create_persistent_volume(cls):
        pass

    @classmethod
    def create_deployment(cls):
        pass

    def create_data_volume(self):
        pvol = persistent_volumes.get_persistent_volume(constants.DATA_VOLUME,
                                                        self.polyaxonfile.run_type)
        self.k8s.create_persistent_volume(pvol)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(constants.DATA_VOLUME)
        self.k8s.create_namespaced_persistent_volume_claim(self.namespace, pvol_claim)
        self.has_data_volume = True

    def create_logs_volume(self):
        pvol = persistent_volumes.get_persistent_volume(constants.LOGS_VOLUME,
                                                        self.polyaxonfile.run_type)
        self.k8s.create_persistent_volume(pvol)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(constants.DATA_VOLUME)
        self.k8s.create_namespaced_persistent_volume_claim(self.namespace, pvol_claim)
        self.has_logs_volume = True

    def create_tmp_volumes(self):
        pvol = persistent_volumes.get_persistent_volume(constants.TMP_VOLUME,
                                                        self.polyaxonfile.run_type)
        self.k8s.create_persistent_volume(pvol)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(constants.DATA_VOLUME)
        self.k8s.create_namespaced_persistent_volume_claim(self.namespace, pvol_claim)
        self.has_tmp_volume = True

    def create_files_volumes(self):
        pvol = persistent_volumes.get_persistent_volume(constants.POLYAXON_FILES_VOLUME,
                                                        self.polyaxonfile.run_type)
        self.k8s.create_persistent_volume(pvol)
        pvol_claim = persistent_volumes.get_persistent_volume_claim(constants.POLYAXON_FILES_VOLUME)
        self.k8s.create_namespaced_persistent_volume_claim(self.namespace, pvol_claim)
        self.has_files_volume = True

    def create_cluster_config_map(self, experiment=0):
        config_map = config_maps.get_cluster_config_map(
            self.polyaxonfile.project.name,
            experiment,
            self.polyaxonfile.get_cluster_def_at(experiment))
        self.k8s.create_namespaced_config_map(self.namespace, config_map)
