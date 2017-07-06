# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

tf.GraphKeys.INPUTS = 'inputs'
tf.GraphKeys.OUTPUTS = 'outputs'
tf.GraphKeys.DROPOUTS = 'dropouts'
tf.GraphKeys.TRAIN_OPS = 'train_ops'
tf.GraphKeys.METRICS = 'metrics'
tf.GraphKeys.LAYER_VARIABLES = 'layer_variables'
tf.GraphKeys.LAYER_TENSOR = 'layer_tensor'
tf.GraphKeys.GRAPH_CONFIG = 'graph_config'
tf.GraphKeys.DATA_PREPROCESSING = 'data_preprocessing'
tf.GraphKeys.DATA_AUGMENTATION = 'data_augmentation'
tf.GraphKeys.LEARNING_RATE = 'learning_rate'
tf.GraphKeys.EXPLORATION_RATE = 'exploration_rate'
tf.GraphKeys.EXCL_RESTORE_VARIABLES = 'excluded_restore_vars'
tf.GraphKeys.MODE = 'mode'
tf.GraphKeys.MODE_OPS = 'mode_ops'
tf.GraphKeys.QUEUES = 'queues'
tf.GraphKeys.PREDICTIONS = 'predictions'
tf.GraphKeys.TRAIN_SUMMARIES = 'train_summaries'
tf.GraphKeys.SUMMARIES_BY_NAMES = 'summaries_by_names'
tf.GraphKeys.GLOBAL_EPISODE = 'global_episode'
tf.GraphKeys.GLOBAL_TIMESTEP = 'global_timestep'

MAPPING_COLLECTION = [tf.GraphKeys.PREDICTIONS, tf.GraphKeys.SUMMARIES_BY_NAMES]
