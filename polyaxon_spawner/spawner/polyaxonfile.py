# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.utils import TaskType

from polyaxon_spawner.spawner.base import K8SSpawner
from polyaxon_spawner.templates import constants


class K8SPolyaxonFileSpawner(K8SSpawner):
    def __init__(self, polyaxonfile, k8s_config=None, namespace='default', in_cluster=False):
        super(K8SPolyaxonFileSpawner, self).__init__(k8s_config=k8s_config,
                                                     namespace=namespace,
                                                     in_cluster=in_cluster)
        self._polyaxonfile = PolyaxonFile.read(polyaxonfile)

    @property
    def spec(self):
        return self._polyaxonfile

    def get_pod_args(self, experiment, task_type, task_id, schedule):
        spec_data = json.dumps(self.spec.get_parsed_data_at(experiment))

        args = [
            "from polyaxon.polyaxonfile.local_runner import start_experiment_run; "
            "start_experiment_run('{polyaxonfile}', '{experiment_id}', "
            "'{task_type}', {task_id}, '{schedule}')".format(
                polyaxonfile=spec_data,
                experiment_id=experiment,
                task_type=task_type,
                task_id=task_id,
                schedule=schedule)]
        return args

    def create_data_volume(self):
        self._create_volume(constants.DATA_VOLUME)
        self.has_data_volume = True

    def create_logs_volume(self):
        self._create_volume(constants.LOGS_VOLUME)
        self.has_logs_volume = True

    def create_files_volumes(self):
        self._create_volume(constants.POLYAXON_FILES_VOLUME)
        self.has_files_volume = True

    def delete_data_volume(self):
        self._delete_volume(constants.DATA_VOLUME)
        self.has_data_volume = False

    def delete_logs_volume(self):
        self._delete_volume(constants.LOGS_VOLUME)
        self.has_logs_volume = False

    def delete_files_volumes(self):
        self._delete_volume(constants.POLYAXON_FILES_VOLUME)
        self.has_files_volume = False

    def delete_volumes(self):
        self.delete_data_volume()
        self.delete_logs_volume()
        self.delete_files_volumes()

    def create_volumes(self):
        self.create_data_volume()
        self.create_logs_volume()
        self.create_files_volumes()

    def create_worker(self, experiment=0):
        n_pods = self.spec.get_cluster_def_at(experiment)[0].get(TaskType.WORKER, 0)
        resources = self.spec.get_worker_resources_at(experiment)
        return self._create_worker(experiment=experiment, resources=resources, n_pods=n_pods)

    def delete_worker(self, experiment=0):
        n_pods = self.spec.get_cluster_def_at(experiment)[0].get(TaskType.WORKER, 0)
        self._delete_worker(experiment=experiment, n_pods=n_pods)

    def create_ps(self, experiment=0):
        n_pods = self.spec.get_cluster_def_at(experiment)[0].get(TaskType.PS, 0)
        resources = self.spec.get_ps_resources_at(experiment)
        return self._create_ps(experiment=experiment, resources=resources, n_pods=n_pods)

    def delete_ps(self, experiment=0):
        n_pods = self.spec.get_cluster_def_at(experiment)[0].get(TaskType.PS, 0)
        self._delete_ps(experiment=experiment, n_pods=n_pods)

    def start_experiment(self, experiment=0):
        self.create_volumes()
        self.create_cluster_config_map(experiment=experiment)
        self.create_master(experiment, resources=self.spec.get_master_resources_at(experiment))
        self.create_worker(experiment)
        self.create_ps(experiment)

    def delete_experiment(self, experiment=0):
        self.delete_volumes()
        self.delete_cluster_config_map(experiment=experiment)
        self.delete_master(experiment)
        self.delete_worker(experiment)
        self.delete_ps(experiment)

    def start_all_experiments(self):
        for xp in range(self.spec.matrix_space):
            self.start_experiment(xp)

    def delete_all_experiments(self):
        for xp in range(self.spec.matrix_space):
            self.delete_experiment(xp)
