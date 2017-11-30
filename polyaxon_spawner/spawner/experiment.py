# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

from polyaxon_schemas.polyaxonfile.polyaxonfile import Specification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import TaskType

from polyaxon_spawner.spawner.base import K8SSpawner


class K8SExperimentSpawner(K8SSpawner):
    def __init__(self,
                 project_id,
                 experiment_id,
                 specification,
                 spec_id=None,
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
        super(K8SExperimentSpawner, self).__init__(k8s_config=k8s_config,
                                                   namespace=namespace,
                                                   in_cluster=in_cluster,
                                                   job_container_name=job_container_name,
                                                   job_docker_image=job_docker_image,
                                                   sidecar_container_name=sidecar_container_name,
                                                   sidecar_docker_image=sidecar_docker_image,
                                                   role_label=role_label,
                                                   type_label=type_label,
                                                   ports=ports,
                                                   use_sidecar=use_sidecar,
                                                   sidecar_config=sidecar_config,
                                                   sidecar_args_fn=sidecar_args_fn)
        self.specification = Specification.read(specification)
        self.project_id = project_id
        self.spec_id = spec_id
        self.experiment_id = experiment_id

    @cached_property
    def project_name(self):
        if self.spec_id:
            return '{}-id{}-spec{}'.format(self.spec.project.name.replace('_', '-'),
                                           self.project_id,
                                           self.spec_id)
        else:
            return '{}-id{}'.format(self.spec.project.name.replace('_', '-'),
                                    self.project_id)

    @property
    def spec(self):
        return self.specification

    def get_pod_args(self, experiment, task_type, task_id, schedule):
        spec_data = json.dumps(self.spec.parsed_data)

        args = [
            "from polyaxon.polyaxonfile.local_runner import start_experiment_run; "
            "start_experiment_run('{polyaxonfile}', '{experiment_id}', "
            "'{task_type}', {task_id}, '{schedule}')".format(
                polyaxonfile=spec_data,
                experiment_id=0,
                task_type=task_type,
                task_id=task_id,
                schedule=schedule)]
        return args

    def create_worker(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)
        resources = self.spec.worker_resources
        return self._create_worker(experiment=self.experiment_id,
                                   resources=resources,
                                   n_pods=n_pods)

    def delete_worker(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)
        self._delete_worker(experiment=self.experiment_id, n_pods=n_pods)

    def create_ps(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.PS, 0)
        resources = self.spec.ps_resources
        return self._create_ps(experiment=self.experiment_id,
                               resources=resources,
                               n_pods=n_pods)

    def delete_ps(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.PS, 0)
        self._delete_ps(experiment=self.experiment_id, n_pods=n_pods)

    def start_experiment(self):
        self.check_data_volume()
        self.check_logs_volume()
        self.create_cluster_config_map(experiment=self.experiment_id)
        master_resp = self.create_master(experiment=self.experiment_id,
                                         resources=self.spec.master_resources)
        worker_resp = self.create_worker()
        ps_resp = self.create_ps()
        return {
            TaskType.MASTER: master_resp,
            TaskType.WORKER: worker_resp,
            TaskType.PS: ps_resp
        }

    def delete_experiment(self):
        self.delete_cluster_config_map(experiment=self.experiment_id)
        self.delete_master(experiment=self.experiment_id)
        self.delete_worker()
        self.delete_ps()

    def get_task_status(self, task_type, task_id):
        return super(K8SExperimentSpawner, self).get_task_status(experiment=self.experiment_id,
                                                                 task_type=task_type,
                                                                 task_id=task_id)

    def get_task_log(self, task_type, task_id, **kwargs):
        return super(K8SExperimentSpawner, self).get_task_log(experiment=self.experiment_id,
                                                              task_type=task_type,
                                                              task_id=task_id,
                                                              **kwargs)

    def get_experiment_status(self):
        self.get_task_log(task_type=TaskType.MASTER, task_id=0)
