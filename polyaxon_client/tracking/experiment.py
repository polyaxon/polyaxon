# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import os

from polyaxon_client import settings
from polyaxon_client.logger import logger
from polyaxon_client.tracking.base import BaseTracker, ensure_in_custer


class Experiment(BaseTracker):
    def __init__(self,
                 project=None,
                 experiment_id=None,
                 client=None,
                 track_logs=None,
                 track_git=None,
                 track_env=None,
                 auto_status=None,
                 schema_response=None):
        super(Experiment, self).__init__(client=client,
                                         track_logs=track_logs,
                                         track_git=track_git,
                                         track_env=track_env)
        self.project = project
        self.experiment_id = experiment_id
        self.auto_status = auto_status
        self.schema_response = schema_response

    def log_metrics(self, **metrics):
        pass

    def log_tags(self, tags, reset=False):
        pass

    def log_params(self, reset=False, **params):
        pass

    def log_status(self, status):
        pass

    def log_data_hash(self, data, data_name='data'):
        try:
            import hashlib

            params = {
                data_name: hashlib.md5(str(data).encode("utf-8")).hexdigest()[:settings.HASH_LENGTH]
            }
            self.log_params(**params)
        except Exception as e:
            logger.warning('Could create data hash %s', e)


def get_cluster_def():
    """Returns cluster definition created by polyaxon.
    {
        "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                   "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "ps": ["plxjob-ps3-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
    }
    :return: dict
    """
    ensure_in_custer()

    cluster = os.getenv('POLYAXON_CLUSTER', None)
    try:
        return json.loads(cluster) if cluster else None
    except (ValueError, TypeError):
        print('Could get cluster definition, '
              'please make sure this is running inside a polyaxon job.')
        return None


def get_task_info():
    """Returns the task info: {"type": str, "index": int}."""
    ensure_in_custer()

    info = os.getenv('POLYAXON_TASK_INFO', None)
    try:
        return json.loads(info) if info else None
    except (ValueError, TypeError):
        print('Could get task info, '
              'please make sure this is running inside a polyaxon job.')
        return None


def get_tf_config(envvar='TF_CONFIG'):
    """
    Returns the TF_CONFIG defining the cluster and the current task.
    if `envvar` is not null, it will set and env variable with `envvar`.
    """
    ensure_in_custer()

    cluster_def = get_cluster_def()
    task_info = get_task_info()
    tf_config = {
        'cluster': cluster_def,
        'task': task_info,
        'model_dir': Experiment.get_outputs_path(),
        'environment': 'cloud'
    }

    if envvar:
        os.environ[envvar] = json.dumps(tf_config)

    return tf_config


def get_experiment_info():
    """
    Returns information about the experiment:
        * project_name
        * experiment_group_name
        * experiment_name
        * project_uuid
        * experiment_group_uuid
        * experiment_uuid
    """
    ensure_in_custer()

    info = os.getenv('POLYAXON_EXPERIMENT_INFO', None)
    try:
        return json.loads(info) if info else None
    except (ValueError, TypeError):
        print('Could get experiment info, '
              'please make sure this is running inside a polyaxon job.')
        return None


def get_declarations():
    """
    Returns all the experiment declarations based on both:
        * declarations section
        * matrix section
    """
    ensure_in_custer()

    declarations = os.getenv('POLYAXON_DECLARATIONS', None)
    try:
        return json.loads(declarations) if declarations else None
    except (ValueError, TypeError):
        print('Could get declarations, '
              'please make sure this is running inside a polyaxon job.')
        return None
