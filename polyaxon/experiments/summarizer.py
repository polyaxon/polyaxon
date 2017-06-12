# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

import tensorflow as tf

from tensorflow.python.framework import ops
from tensorflow.python.ops import clip_ops

from polyaxon.libs.utils import track, get_tracked


class SummaryOptions(object):
    ACTIVATIONS = 'activations'
    LOSS = 'loss'
    GRADIENTS = 'gradients'
    VARIABLES = 'variables'
    LEARNING_RATE = 'learning_rate'
    IMAGE_INPUT = 'image_input'
    IMAGE_RESULT = 'image_result'
    IMAGE_GENERATED = 'image_generated'

    ALL = [ACTIVATIONS, LOSS, GRADIENTS, VARIABLES, LEARNING_RATE]
    VALUES = [ACTIVATIONS, LOSS, GRADIENTS, VARIABLES, LEARNING_RATE,
              IMAGE_INPUT, IMAGE_RESULT, IMAGE_GENERATED]

    @classmethod
    def validate(cls, summaries):
        if isinstance(summaries, six.string_types):
            if summaries == 'all':
                return cls.ALL
            if summaries in cls.VALUES:
                return [summaries]

        if isinstance(summaries, (list, tuple)):
            if 'all' in summaries:
                return cls.ALL
            if not set(summaries) - set(cls.VALUES):
                return summaries

        raise ValueError("The summary `{}` provided is not supported, "
                         "must be a subset of `{}`".format(summaries, cls.VALUES))


class SummaryTypes(object):
    SCALAR = 'scalar'
    HISTOGRAM = 'histogram'
    IMAGE = 'image'

    VALUES = [SCALAR, HISTOGRAM, IMAGE]

    @classmethod
    def check_summary_type(cls, stype):
        if stype not in cls.VALUES:
            raise ValueError("Unknown summary type: `{}`".format(stype))

    @classmethod
    def summarize(cls, stype, name, value, **kwargs):
        cls.check_summary_type(stype)

        if stype == cls.HISTOGRAM:
            return tf.summary.histogram(name=name, values=value, **kwargs)
        if stype == cls.SCALAR:
            return tf.summary.scalar(name=name, tensor=value, **kwargs)
        if stype == cls.IMAGE:
            return tf.summary.image(name=name, tensor=value, **kwargs)


def add_learning_rate_summaries():
    learning_rate = get_tracked(tf.GraphKeys.LEARNING_RATE)
    if not learning_rate:
        return []

    return [get_summary(SummaryTypes.SCALAR, 'learning_rate', learning_rate[0])]


def add_loss_summaries(total_loss, loss):
    """Adds loss scalar summaries.

    Args:
        total_loss: `Tensor`. The total loss (Regression loss + regularization losses).
        loss: `Tensor`. Regression loss.

    Returns:
        The list of created loss summaries.
    """
    summaries = []

    if total_loss is not None:
        summaries.append(get_summary(SummaryTypes.SCALAR, total_loss.op.name, total_loss))

    summaries.append(get_summary(SummaryTypes.SCALAR, 'Loss', loss))

    for regu_loss in get_tracked(tf.GraphKeys.REGULARIZATION_LOSSES):
        summaries.append(get_summary(SummaryTypes.SCALAR, regu_loss.op.name, regu_loss))
    return summaries


def add_activations_summary(activation_ops):
    """Adds histogram and scalar summary for given activations.

    Args:
        activation_ops: A list of `Tensor`. The activations to summarize.

    Returns:
        The list of created activation summaries.
    """

    summaries = []
    for activation in activation_ops:
        activation_name = activation.op.name + '/Activations'
        summaries.append(get_summary(SummaryTypes.HISTOGRAM, activation_name,  activation))

        activation_name = activation.op.name + '/Activation'
        summaries.append(get_summary(SummaryTypes.SCALAR, activation_name,
                                     tf.nn.zero_fraction(value=activation)))
    return summaries


def add_gradients_summary(grads):
    """Add histogram summary for given gradients and scalar summary for clipped gradients.

    Args:
        grads: A list of `Tensor`. The gradients to summarize.

    Returns:
        The list of created gradient summaries.

    """

    # Add histograms for gradients.
    summary = []
    for gradient, var in grads:
        if isinstance(gradient, ops.IndexedSlices):
            grad_values = gradient.values
        else:
            grad_values = gradient

        if grad_values is not None:
            summary_name = var.op.name + '/Gradients'
            summary.append(get_summary(SummaryTypes.HISTOGRAM, summary_name, grad_values))

            summary_norm_name = var.op.name + '/GradientsNorm'
            summary.append(get_summary(SummaryTypes.SCALAR, summary_norm_name,
                                       clip_ops.global_norm([grad_values])))

        summary.append(get_summary(SummaryTypes.SCALAR, 'ClippedGradientNorm',
                                   clip_ops.global_norm(list(zip(*grads))[0])))
    return summary


def add_trainable_vars_summary(variables):
    """Adds histogram summary for given variables weights.

    Args:
        variables: A list of `Variable`. The variables to summarize.

    Returns:
        The list of created weights summaries.

    """
    summary = []
    for var in variables:
        summary.append(get_summary(SummaryTypes.HISTOGRAM, var.op.name, var))
    return summary


def add_image_summary(value, op_name=None):
    return [get_summary(SummaryTypes.IMAGE, op_name or value.op.name, value)]


def _summary_for_name(name):
    """Gets a summary for a given name.

    Args:
        name: `str`. The summary name.

    Returns:
        The summary if it exists or `None` otherwise

    """
    return get_tracked(tf.GraphKeys.SUMMARIES_BY_NAMES).get(name)


def get_summary(stype, name, value=None, collect=True, **kwargs):
    """Creates or retrieves a summary.

    It keep tracks of all graph summaries through SUMMARIES_BY_NAMES collection.
    If a summary tags already exists, it will return that summary tensor.

    Args:
        stype: `str`. Summary type: 'histogram', 'scalar' or 'image'.
        name: `str`. The summary tag (name).
        value: `Tensor`. The summary initialization value. Default: None.
        collect: `boolean`. Adds the summary to the summaries collection.

    Returns:
        The summary `Tensor`.

    """
    summary = _summary_for_name(name)

    if summary is None:
        summary = SummaryTypes.summarize(stype, name, value, **kwargs)

        track({name: summary}, collection=tf.GraphKeys.SUMMARIES_BY_NAMES)
        if collect:
            track(summary, collection=tf.GraphKeys.TRAIN_SUMMARIES)

    return summary
