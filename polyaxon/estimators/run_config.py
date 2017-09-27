# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.estimator import run_config

from polyaxon_schemas import settings


class RunConfig(run_config.RunConfig):
    CONFIG = settings.RunConfig

    def __init__(self):
        super(RunConfig, self).__init__()
        self._cluster_spec = None

    @property
    def cluster_spec(self):
        return self._cluster_spec

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
