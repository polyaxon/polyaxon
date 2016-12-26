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
tf.GraphKeys.LEARNING_RATE_VARS = 'learning_rate_vars'
tf.GraphKeys.EXCL_RESTORE_VARIABLES = 'excluded_restore_vars'
tf.GraphKeys.MODE = 'mode'
tf.GraphKeys.MODE_OPS = 'mode_ops'
tf.GraphKeys.QUEUES = 'queues'
tf.GraphKeys.PREDICTIONS = 'predictions'
