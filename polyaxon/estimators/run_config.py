# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from tensorflow.python.estimator import run_config

from polyaxon_schemas import settings


class RunConfig(run_config.RunConfig):
    CONFIG = settings.RunConfig

    @classmethod
    def from_config(cls, config):
        if not isinstance(config, cls.CONFIG):
            config = cls.CONFIG.from_dict(config)

        params = config.to_dict()
        return cls(**params)

    @classmethod
    def read_configs(cls, config_values):
        config_values = cls._read_configs(config_values)
        gpu_allow_growth = config_values.pop('gpu_allow_growth', False)
        log_device_placement = config_values.pop('log_device_placement', False)
        config = cls(**config_values)
        config.tf_config.gpu_options.allow_growth = gpu_allow_growth
        config.tf_config.log_device_placement = log_device_placement
        return config

    @staticmethod
    def create_cluster_config(cluster_config):
        """Sets the cluster config to the environment variable `TF_CONFIG`.

        Args:
            cluster_config: `dict`. Represents the cluster config dictionary.
        """
        # First we need to check the type of the task for this env
        task_type = os.environ.get('task_type')
        if task_type not in ['master', 'ps', 'worker']:
            return

        try:
            task_id = int(os.environ.get('task_index'))
        except TypeError:
            return

        config = {
            'environment': cluster_config.pop('environment', 'cloud'),
            'cluster': cluster_config,
            'task': {'type': task_type, 'index': task_id}
        }
        # Set the cluster config in the environment variable `TF_CONFIG`.
        os.environ['TF_CONFIG'] = json.dumps(config)
