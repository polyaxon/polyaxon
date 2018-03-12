# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import logging

from polyaxon_schemas.polyaxonfile.specification.frameworks import TensorflowSpecification
from polyaxon_schemas.utils import TaskType

from spawners.tensorflow_spawner import TensorflowSpawner

logger = logging.getLogger('polyaxon.spawners.polyaxon')


class PolyaxonSpawner(TensorflowSpawner):
    def get_pod_command_args(self, task_type, task_idx, schedule):
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

    def create_master(self, resources=None):
        command, args = self.get_pod_command_args(task_type=TaskType.MASTER,
                                                  task_idx=0,
                                                  schedule='train_and_evaluate')
        env_vars = self.get_env_vars(task_type=TaskType.MASTER, task_idx=0)
        return self._create_pod(task_type=TaskType.MASTER,
                                task_idx=0,
                                command=command,
                                args=args,
                                sidecar_args_fn=self.sidecar_args_fn,
                                env_vars=env_vars,
                                resources=resources)

    def _create_workers(self, resources, n_pods):
        resp = []
        for i in range(n_pods):
            command, args = self.get_pod_command_args(task_type=TaskType.WORKER,
                                                      task_idx=i,
                                                      schedule='train')
            env_vars = self.get_env_vars(task_type=TaskType.WORKER, task_idx=i)
            resp.append(self._create_pod(task_type=TaskType.WORKER,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         sidecar_args_fn=self.sidecar_args_fn,
                                         env_vars=env_vars,
                                         resources=resources.get(i)))
        return resp

    def create_workers(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.WORKER, 0)

        cluster, is_distributed, = self.spec.cluster_def
        resources = TensorflowSpecification.get_worker_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return self._create_workers(resources=resources, n_pods=n_pods)

    def _create_servers(self, resources, n_pods):
        resp = []
        for i in range(n_pods):
            command, args = self.get_pod_command_args(task_type=TaskType.PS,
                                                      task_idx=i,
                                                      schedule='run_std_server')
            env_vars = self.get_env_vars(task_type=TaskType.PS, task_idx=i)
            resp.append(self._create_pod(task_type=TaskType.PS,
                                         task_idx=i,
                                         command=command,
                                         args=args,
                                         sidecar_args_fn=self.sidecar_args_fn,
                                         env_vars=env_vars,
                                         resources=resources.get(i)))

    def create_servers(self):
        n_pods = self.spec.cluster_def[0].get(TaskType.PS, 0)
        cluster, is_distributed, = self.spec.cluster_def
        resources = TensorflowSpecification.get_ps_resources(
            environment=self.spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        return self._create_servers(resources=resources, n_pods=n_pods)
