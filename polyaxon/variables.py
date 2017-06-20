# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

import tensorflow as tf

from polyaxon.libs import getters


@tf.contrib.framework.add_arg_scope
def variable(name, shape=None, dtype=tf.float32, initializer=None, regularizer=None,
             trainable=True, collections=None, device='', restore=True):
    """Instantiate a new variable.

    Args:
        name: `str`. A name for this variable.
        shape: list of `int`. The variable shape (optional).
        dtype: `type`. The variable data type.
        initializer: `str` or `Tensor`. The variable initialization.
        regularizer: `str` or `Tensor`. The variable regularizer.
        trainable: `bool`. If True, this variable weights will be trained.
        collections: `str`. A collection to add the new variable to (optional).
        device: `str`. Device ID to store the variable. Default: '/cpu:0'.
        restore: `bool`. Restore or not this variable when loading a pre-trained model.

    Returns:
        A Variable.
    """

    if isinstance(initializer, six.string_types):
        initializer = getters.get_initializer(initializer)
    # Remove shape param if initializer is a Tensor
    if not callable(initializer) and isinstance(initializer, tf.Tensor):
        shape = None

    if isinstance(regularizer, six.string_types):
        regularizer = getters.get_regularizer(regularizer)

    with tf.device(device_name_or_function=device):
        var = tf.get_variable(name=name,
                              shape=shape,
                              dtype=dtype,
                              initializer=initializer,
                              regularizer=regularizer,
                              trainable=trainable,
                              collections=collections)

        if not restore:
            tf.add_to_collection(name=tf.GraphKeys.EXCL_RESTORE_VARIABLES, value=var)  # @TODO adapt restoring saver

        return var
