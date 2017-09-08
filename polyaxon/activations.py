# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.ops import clip_ops

from polyaxon.libs.utils import get_name_scope, track


def built_activation(fct, name, collect):
    """Builds the metric function.

    Args:
        fct: the activation function to build.
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def activation(x):
        x = fct(x, name=name)
        if collect:
            track(x, tf.GraphKeys.ACTIVATIONS)
        return x

    return activation


def linear(name='Linear', collect=False):
    """Computes linear/identity function.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def _linear(x, name):
        with get_name_scope(name=name):
            return x

    return built_activation(_linear, name, collect)


def tanh(name=None, collect=False):
    """Computes hyperbolic tangent of x element-wise.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.tanh, name, collect)


def hard_sigmoid(name='HardSigmoid', collect=False):
    """Segment-wise linear approximation of sigmoid.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def _hard_sigmoid(x, name):
        with get_name_scope(name=name):
            return clip_ops.clip_by_value(x, clip_value_min=0., clip_value_max=1.)

    return built_activation(_hard_sigmoid, name, collect)


def sigmoid(name=None, collect=False):
    """Computes sigmoid of `x` element-wise: `y = 1 / (1 + exp(-x))`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.sigmoid, name, collect)


def softmax(name=None, collect=False):
    """Computes softmax activations.

    For each batch `i` and class `j` we have
        `softmax[i, j] = exp(logits[i, j]) / sum(exp(logits[i]))`

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.softmax, name, collect)


def softplus(name=None, collect=False):
    """Computes softplus. `log(exp(features) + 1)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.softplus, name, collect)


def softsign(name=None, collect=False):
    """Computes softsign: `features / (abs(features) + 1)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.softsign, name, collect)


def relu(name=None, collect=False):
    """Computes ReLU, rectified linear: `max(features, 0)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.relu, name, collect)


def relu6(name=None, collect=False):
    """Computes Rectified Linear 6: `min(max(features, 0), 6)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.relu6, name, collect)


def elu(name=None, collect=False):
    """Computes Exponential Linear Unit.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.elu, name, collect)


def selu(name='Selu', collect=False):
    """Scaled Exponential Linear Unit. (Klambauer et al., 2017).

    Arguments:
        x: A tensor or variable to compute the activation function for.

    Returns:
      Tensor with the same shape and dtype as `x`.

    References:
        - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)
    """

    def _selu(x, name=name):
        with get_name_scope(name=name):
            alpha = 1.6732632423543772848170429916717
            scale = 1.0507009873554804934193349852946
            return scale * tf.nn.elu(x, alpha)

    return built_activation(_selu, name, collect)


def crelu(name=None, collect=False):
    """Computes Concatenated ReLU.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.crelu, name, collect)


ACTIVATIONS = {
    'linear': linear,
    'tanh': tanh,
    'sigmoid': sigmoid,
    'softmax': softmax,
    'softplus': softplus,
    'softsign': softsign,
    'relu': relu,
    'relu6': relu6,
    'elu': elu,
    'crelu': crelu
}
