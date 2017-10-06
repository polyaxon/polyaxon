# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.ops import clip_ops

from polyaxon.libs.utils import get_name_scope, track


def built_activation(x, collect):
    """Builds the metric function.

    Args:
        x: activated tensor.
        collect: whether to collect this metric under the metric collection.
    """

    if collect:
        track(x, tf.GraphKeys.ACTIVATIONS)
    return x


def linear(name='Linear', collect=True):
    """Computes linear/identity function.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def linear(x):  # pylint: disable=redefined-outer-name
        return built_activation(x, collect)

    return linear


def tanh(name=None, collect=True):
    """Computes hyperbolic tangent of x element-wise.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def tanh(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.tanh(x, name), collect)

    return tanh


def hard_sigmoid(name='HardSigmoid', collect=True):
    """Segment-wise linear approximation of sigmoid.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def hard_sigmoid(x):  # pylint: disable=redefined-outer-name
        with get_name_scope(name=name):
            x = clip_ops.clip_by_value(x, clip_value_min=0., clip_value_max=1.)
            return built_activation(x, collect)

    return hard_sigmoid


def sigmoid(name=None, collect=True):
    """Computes sigmoid of `x` element-wise: `y = 1 / (1 + exp(-x))`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def sigmoid(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.sigmoid(x, name), collect)

    return sigmoid


def softmax(name=None, collect=True):
    """Computes softmax activations.

    For each batch `i` and class `j` we have
        `softmax[i, j] = exp(logits[i, j]) / sum(exp(logits[i]))`

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def softmax(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.softmax(x, name), collect)

    return softmax


def softplus(name=None, collect=True):
    """Computes softplus. `log(exp(features) + 1)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def softplus(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.softplus(x, name), collect)

    return softplus


def softsign(name=None, collect=True):
    """Computes softsign: `features / (abs(features) + 1)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def softsign(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.softsign(x, name), collect)

    return softsign


def relu(name=None, collect=True):
    """Computes ReLU, rectified linear: `max(features, 0)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def relu(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.relu(x, name), collect)

    return relu


def relu6(name=None, collect=True):
    """Computes Rectified Linear 6: `min(max(features, 0), 6)`.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def relu6(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.relu6(x, name), collect)

    return relu6


def elu(name=None, collect=True):
    """Computes Exponential Linear Unit.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def elu(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.elu(x, name), collect)

    return elu


def selu(name='Selu', collect=True):
    """Scaled Exponential Linear Unit. (Klambauer et al., 2017).

    Arguments:
        x: A tensor or variable to compute the activation function for.

    Returns:
      Tensor with the same shape and dtype as `x`.

    References:
        - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)
    """

    def selu(x):  # pylint: disable=redefined-outer-name
        with get_name_scope(name=name):
            alpha = 1.6732632423543772848170429916717
            scale = 1.0507009873554804934193349852946
            x = scale * tf.nn.elu(x, alpha)
            return built_activation(x, collect)

    return selu


def crelu(name=None, collect=True):
    """Computes Concatenated ReLU.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    def crelu(x):  # pylint: disable=redefined-outer-name
        return built_activation(tf.nn.crelu(x, name), collect)

    return crelu


ACTIVATIONS = {
    'linear': linear,
    'tanh': tanh,
    'sigmoid': sigmoid,
    'hard_sigmoid': hard_sigmoid,
    'softmax': softmax,
    'softplus': softplus,
    'softsign': softsign,
    'relu': relu,
    'relu6': relu6,
    'elu': elu,
    'crelu': crelu
}
