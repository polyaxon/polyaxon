# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import logging

from polyaxon_schemas.polyaxonfile.specification.frameworks import TensorflowSpecification
from polyaxon_schemas.utils import TaskType

from spawners.tensorflow_spawner import TensorflowSpawner

logger = logging.getLogger('polyaxon.spawners.polyaxon')


class PolyaxonSpawner(TensorflowSpawner):

    @staticmethod
    def _get_schedule(task_type):
        if task_type == TaskType.MASTER:
            return 'train_and_evaluate'
        if task_type == TaskType.WORKER:
            return 'train'
        if task_type == TaskType.PS:
            return 'run_std_server'

    def get_pod_command_args(self, task_type, task_idx):
        spec_data = json.dumps(self.spec.parsed_data)
        schedule = self._get_schedule(task_type=task_type)

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
