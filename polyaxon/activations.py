# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.libs import getters
from polyaxon.libs.utils import get_name_scope, get_shape, track
from polyaxon.variables import variable


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


def leaky_relu(alpha=0.1, name='LeakyReLU', collect=False):
    """Modified version of ReLU, introducing a nonzero gradient for negative input.

    Args:
        alpha: `int`, the multiplier.
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def _leak_relu(x, name):
        with get_name_scope(name):
            x = tf.nn.relu(features=x)
            m_x = tf.nn.relu(features=-x)
            x -= alpha * m_x
            return x

    return built_activation(_leak_relu, name, collect)


def prelu(channel_shared=False, weights_init='zeros', restore=True, name='PReLU', collect=False):
    """Parametric Rectified Linear Unit.

    Args:
        channel_shared:
        weights_init:
        restore:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """

    def _prelu(x, name):
        with get_name_scope(name):
            if channel_shared:
                w_shape = (1,)
            else:
                w_shape = get_shape(x)[-1:]

            w_init = getters.get_initializer(weights_init)
            alphas = variable(shape=w_shape, initializer=w_init, restore=restore, name="alphas")

            x = tf.nn.relu(features=x) + tf.multiply(x=alphas, y=(x - tf.abs(x))) * 0.5
            x.alphas = alphas
            return x

    return built_activation(_prelu, name, collect)


def elu(name=None, collect=False):
    """Computes Exponential Linear Unit.

    Args:
        name: operation name.
        collect: whether to collect this metric under the metric collection.
    """
    return built_activation(tf.nn.elu, name, collect)


def crelu(name='CRelu', collect=False):
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
    'leaky_relu': leaky_relu,
    'elu': elu,
    'crelu': crelu
}
