# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import six

import tensorflow as tf

from tensorflow.python.estimator import run_config

from polyaxon_schemas import settings
from polyaxon_schemas.utils import TaskType


def _validate_properties(new_copy):
    run_config._validate_properties(new_copy)  # pylint: disable=protected-access

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


def _get_master(cluster_spec, task_type, task_id):
    """Returns the appropriate string for the TensorFlow master."""
    if not cluster_spec:
        return ''

    # If there is only one node in the cluster, do things locally.
    jobs = cluster_spec.jobs
    if len(jobs) == 1 and len(cluster_spec.job_tasks(jobs[0])) == 1:
        return ''

    # Lookup the master in cluster_spec using task_type and task_id,
    # if possible.
    if task_type:
        if task_type not in jobs:
            raise ValueError(
                '%s is not a valid task_type in the cluster_spec:\n'
                '%s\n\n'
                'Note that these values may be coming from the TF_CONFIG environment '
                'variable.' % (task_type, cluster_spec))
        addresses = cluster_spec.job_tasks(task_type)
        if task_id >= len(addresses) or task_id < 0:
            raise ValueError(
                '%d is not a valid task_id for task_type %s in the '
                'cluster_spec:\n'
                '%s\n\n'
                'Note that these value may be coming from the TF_CONFIG environment '
                'variable.' % (task_id, task_type, cluster_spec))
        return 'grpc://' + addresses[task_id]


class RunConfig(run_config.RunConfig):
    CONFIG = settings.RunConfig

    def __init__(self):
        super(RunConfig, self).__init__()
        self._cluster_spec = None
        self._task_type = TaskType.WORKER
        self._task_id = 0
        self._session_config = tf.ConfigProto()

    @property
    def cluster_spec(self):
        return self._cluster_spec

    @property
    def task_type(self):
        return self._task_type

    @property
    def task_id(self):
        return self._task_id

    @property
    def is_chief(self):
        if self.cluster_spec is None:
            return True
        return self.task_type == TaskType.MASTER and self.task_id == 0

    @property
    def master(self):
        if self.cluster_spec is None:
            return ''
        return _get_master(self.cluster_spec, self.task_type, self.task_id)

    @property
    def num_ps_replicas(self):
        if self.cluster_spec is None:
            return 0
        return self.cluster_spec.num_tasks('ps')

    @property
    def num_worker_replicas(self):
        if self.cluster_spec is None:
            return 1
        return self.cluster_spec.num_tasks('worker')

    @property
    def is_distributed(self):
        return self.num_ps_replicas + self.num_worker_replicas > 1

    @classmethod
    def from_config(cls, config):
        if not isinstance(config, cls.CONFIG):
            config = cls.CONFIG.from_dict(config)

        config_params = {}
        if config.session:
            config_params['session_config'] = cls.get_session_config(config.session)
        if config.cluster:
            config_params['cluster_spec'] = cls.get_cluster_spec_config(config.cluster)

        params = config.to_dict()
        params.pop('cluster', None)
        params.pop('session', None)
        config_params.update(params)
        return cls().replace(**config_params)

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

        run_config._validate_save_ckpt_with_replaced_keys(
            new_copy, kwargs.keys())  # pylint: disable=protected-access
        run_config._validate_properties(new_copy)  # pylint: disable=protected-access
        return new_copy
