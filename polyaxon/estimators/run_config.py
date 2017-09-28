# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import six

import tensorflow as tf

from tensorflow.python.estimator import run_config

from polyaxon_schemas import settings


TaskType = run_config.TaskType


def _validate_properties(new_copy):
    run_config._validate_properties(new_copy)

    def _validate(property_name, cond, message):
        property_value = getattr(new_copy, property_name)
        if property_value is not None and not cond(property_value):
            raise ValueError(message)

    _validate('cluster_spec', lambda spec: isinstance(spec, settings.ClusterConfig),
              message="`cluster_spec` must be an instance of `ClusterConfig`")

    task_types = [TaskType.MASTER, TaskType.PS, TaskType.WORKER]
    _validate('task_type', lambda task_type: task_type in task_types,
              message="`task_type` must be one o `{}`".format(task_types))

    _validate('task_id', lambda task_id: isinstance(task_id, int),
              message="`task_id` must be an integer.")

    num_tasks = new_copy.cluster_spec.num_tasks(new_copy.task_type)
    _validate('task_id', lambda t_id: t_id < num_tasks,
              message="`task_id` {} for task type {} must "
                      "be one of the {} tasks.".format(new_copy.task_id,
                                                       new_copy.task_type,
                                                       num_tasks))


class RunConfig(run_config.RunConfig):
    CONFIG = settings.RunConfig

    def __init__(self):
        super(RunConfig, self).__init__()
        self._cluster_spec = None
        self._task_type = TaskType.WORKER
        self._task_id = 0

    @property
    def cluster_spec(self):
        return self._cluster_spec

    @property
    def task_type(self):
        return self._task_type

    @property
    def task_id(self):
        return self._task_id

    @classmethod
    def from_config(cls, config):
        if not isinstance(config, cls.CONFIG):
            config = cls.CONFIG.from_dict(config)

        config_params = {}
        if config.session:
            config_params['session_config'] = cls.get_session_config(config.session)
        if config.cluster:
            config_params['cluster_spec'] = cls.get_session_config(config.cluster)

        params = config.to_dict()
        return cls().replace(**params)

    @staticmethod
    def get_cluster_spec_config(config):
        if not isinstance(config, settings.ClusterConfig):
            raise ValueError('`config` must be an instance of `schemas.ClusterConfig`')

        return tf.train.ClusterSpec(config.to_dict())

    @classmethod
    def get_session_config(cls, config):
        if not isinstance(config, settings.SessionConfig):
            raise ValueError('`config` must be an instance of `schemas.SessionConfig`')

        session_config = {}
        if config.gpu_options:
            session_config['gpu_options'] = cls.get_gpu_options(config.gpu_options)

        params = config.to_dict()
        params.pop('gpu_options', None)
        params.pop('index', None)
        session_config.update(params)

        return tf.ConfigProto(**session_config)

    @staticmethod
    def get_gpu_options(config):
        if not isinstance(config, settings.GPUOptionsConfig):
            raise ValueError('`config` must be an instance of `schemas.GPUOptionsConfig`')
        return tf.GPUOptions(**config.to_dict())

    def _replace(self, allowed_properties_list=None, **kwargs):
        """See `replace`.

        N.B.: This implementation assumes that for key named "foo", the underlying
        property the RunConfig holds is "_foo" (with one leading underscore).

        Args:
          allowed_properties_list: The property name list allowed to be replaced.
          **kwargs: keyword named properties with new values.

        Raises:
          ValueError: If any property name in `kwargs` does not exist or is not
            allowed to be replaced, or both `save_checkpoints_steps` and
            `save_checkpoints_secs` are set.

        Returns:
          a new instance of `RunConfig`.
        """

        new_copy = copy.deepcopy(self)

        for key, new_value in six.iteritems(kwargs):
            setattr(new_copy, '_' + key, new_value)
            continue

        run_config._validate_save_ckpt_with_replaced_keys(new_copy, kwargs.keys())
        run_config._validate_properties(new_copy)
        return new_copy
