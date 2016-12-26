# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.ops import math_ops as tf_math_ops

from polyaxon.libs.utils import get_name_scope, track


def built_regularizer(fct, collect):
    """ Builds the regularizer function.

    Args:
        fct: the metric function to build.
        collect: whether to collect this metric under the metric collection.
    """
    def regularizer(x):
        x = fct(x)
        if collect:
            track(x, tf.GraphKeys.REGULARIZATION_LOSSES)
        return x

    return regularizer


def l2_regularizer(scale=0.001, name='l2Regularizer', collect=True):
    """Returns a function that can be used to apply L2 regularization to a tensor.

    Computes half the L2 norm of a tensor without the `sqrt`:

      output = sum(t ** 2) / 2 * wd

    Args:
        x: `Tensor`. The tensor to apply regularization.
        scale: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
        name: `str` name of the app.
        scope: `str` scope to add the op to.
        collect: add to regularization losses

    Returns:
        The regularization `Tensor`.
    """

    def inner_regularizer(x):
        return tf.multiply(x=tf.nn.l2_loss(x), y=scale, name=name)

    return built_regularizer(inner_regularizer, collect)


def l1_regularizer(scale=0.001, name='l1Regularizer', collect=True):
    """Returns a function that can be used to apply L1 regularization to a tensor.

    Computes the L1 norm of a tensor:

      output = sum(|t|) * scale

    Args:
        x: `Tensor`. The tensor to apply regularization.
        scale: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
        name: name of the app.
        collect: add to regularization losses

    Returns:
        The regularization `Tensor`.
    """

    def inner_regularizer(x):
        return tf.multiply(x=tf.reduce_sum(tf.abs(x)), y=scale, name=name)

    return built_regularizer(inner_regularizer, collect)


def l2_l1_regularizer(scale_l1=0.001, scale_l2=0.001, name='l2l1Regularizer', collect=True):
    """Returns a function that can be used to apply L2 L1 regularization to a tensor.

    Computes the L2 and L1 norm of a tensor:

    Args:
        x: `Tensor`. The tensor to apply regularization.
        scale_l1: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
        scale_l2: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
        name: name of the app.
        collect: add to regularization losses

    Returns:
        The regularization `Tensor`.
    """
    def inner_regularizer(x):
        with get_name_scope(name, [x]) as _name:
            regularizer_tensors = [l1_regularizer(scale_l1)(x),
                                   l2_regularizer(scale_l2)(x)]
            tf_math_ops.add_n(regularizer_tensors, name=_name)

    return built_regularizer(inner_regularizer, collect)


REGULIZERS = {
    'l1_regularizer': l1_regularizer,
    'l2_regularizer': l2_regularizer,
    'l2_l1_regularizer': l2_l1_regularizer
}
