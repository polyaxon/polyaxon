# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import tensorflow as tf

from tensorflow.python.ops import math_ops, array_ops

from polyaxon.libs.utils import EPSILON, clip, get_name_scope


def check_loss_data(y_true, y_pred, logits=False):
    if logits:
        y_pred = tf.convert_to_tensor(y_pred)
        y_true = math_ops.cast(y_true, y_pred.dtype)
    else:
        y_pred = math_ops.to_float(y_pred)
        y_true = math_ops.to_float(y_true)

    y_pred.get_shape().assert_is_compatible_with(y_true.get_shape())
    return y_true, y_pred


def built_loss(fct, weights, name, scope, collect, logits=False):
    """ Builds the loss function.

    Args:
        fct: the loss function to build.
        name: operation name.
        scope: operation scope.
        collect: whether to collect this metric under the metric collection.
    """
    def loss(y_true, y_pred):
        """
        Args:
            y_pred: `Tensor` of `float` type. Predicted values.
            y_true: `Tensor` of `float` type. Targets (labels).

        Returns:
            `Float`. The calculated loss.
        """
        loss_collection = tf.GraphKeys.LOSSES if collect else None
        with get_name_scope(scope, name, (y_true, y_pred, weights)) as scope_:
            y_true, y_pred = check_loss_data(y_true, y_pred, logits)
            losses = fct(y_true, y_pred)
            weighted_loss = tf.losses.compute_weighted_loss(
                losses, weights, scope_, loss_collection)
        return losses, weighted_loss
    return loss


def absolute_difference(weights=1.0, name='AbsoluteDifference', scope=None, collect=True):
    """Adds an Absolute Difference loss to the training procedure.

    `weights` acts as a coefficient for the loss. If a scalar is provided, then
    the loss is simply scaled by the given value. If `weights` is a `Tensor` of
    shape `[batch_size]`, then the total loss for each sample of the batch is
    rescaled by the corresponding element in the `weights` vector. If the shape of
    `weights` matches the shape of `predictions`, then the loss of each
    measurable element of `predictions` is scaled by the corresponding value of
    `weights`.

    Args:
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        scope: operation scope.
        collect: whether to collect this metric under the metric collection.

    Returns:
        A scalar `Tensor` representing the loss value.
    """
    def inner_loss(y_true, y_pred):
        losses = math_ops.abs(math_ops.subtract(y_pred, y_true))
        return losses

    return built_loss(inner_loss, weights, name, scope, collect)


def log_loss(weights=1.0, epsilon=1e-7, name='LogLoss', scope=None, collect=True):
    def inner_loss(y_true, y_pred):
        losses = -math_ops.multiply(
            y_true,
            math_ops.log(y_pred + epsilon)) - math_ops.multiply(
            (1 - y_true), math_ops.log(1 - y_pred + epsilon))
        return losses

    return built_loss(inner_loss, weights, name, scope, collect)


def mean_squared_error(weights=1.0, name='MeanSquaredError', scope=None, collect=True):
    """Computes Mean Square Loss.

    Args:
        weights: Coefficients for the loss a `scalar`.
        scope: scope to add the op to.
        name: name of the op.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        losses = math_ops.square(math_ops.subtract(y_pred, y_true))
        return losses
    return built_loss(inner_loss, weights, name, scope, collect)


def huber_loss(weights=1.0, clip=0.0, name='HuberLoss', scope=None, collect=True):
    """Computes Huber Loss for DQN.

    [Wikipedia link](https://en.wikipedia.org/wiki/Huber_loss)
    [DeepMind link](https://sites.google.com/a/deepmind.com/dqn/)

    Args:
        weights: Coefficients for the loss a `scalar`.
        scope: scope to add the op to.
        name: name of the op.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        delta = math_ops.abs(math_ops.subtract(y_pred, y_true))
        losses = math_ops.square(delta)
        if clip > 0.0:
            losses = tf.where(delta < clip, 0.5 * losses, delta - 0.5)

        return losses
    return built_loss(inner_loss, weights, name, scope, collect)


def clipped_delta_loss(weights=1.0, clip_value_min=-1., clip_value_max=1., name='HuberLoss',
                       scope=None, collect=True):
    """Computes clipped delta Loss for DQN.

    [Wikipedia link](https://en.wikipedia.org/wiki/Huber_loss)
    [DeepMind link](https://sites.google.com/a/deepmind.com/dqn/)

    Args:
        weights: Coefficients for the loss a `scalar`.
        scope: scope to add the op to.
        name: name of the op.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        delta = math_ops.subtract(y_pred, y_true)
        losses = tf.clip_by_value(delta,
                                  clip_value_min=clip_value_min, clip_value_max=clip_value_max)
        losses = tf.square(losses)

        return losses
    return built_loss(inner_loss, weights, name, scope, collect)


def softmax_cross_entropy(weights=1.0, label_smoothing=0, name='SoftmaxCrossEntropy', scope=None,
                          collect=True):
    """Computes Softmax Cross entropy (softmax categorical cross entropy).

    Computes softmax cross entropy between y_pred (logits) and
    y_true (labels).

    Measures the probability error in discrete classification tasks in which
    the classes are mutually exclusive (each entry is in exactly one class).
    For example, each CIFAR-10 image is labeled with one and only one label:
    an image can be a dog or a truck, but not both.

    **WARNING:** This op expects unscaled logits, since it performs a `softmax`
    on `y_pred` internally for efficiency.  Do not call this op with the
    output of `softmax`, as it will produce incorrect results.

    `y_pred` and `y_true` must have the same shape `[batch_size, num_classes]`
    and the same dtype (either `float32` or `float64`). It is also required
    that `y_true` (labels) are binary arrays (For example, class 2 out of a
    total of 5 different classes, will be define as [0., 1., 0., 0., 0.])

    Args:
        weights: Coefficients for the loss a `scalar`.
        label_smoothing: If greater than `0` then smooth the labels.
        scope: scope to add the op to.
        name: name of the op.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        if label_smoothing > 0:
            num_classes = math_ops.cast(array_ops.shape(y_true)[1], y_pred.dtype)
            smooth_positives = 1.0 - label_smoothing
            smooth_negatives = label_smoothing / num_classes
            y_true = y_true * smooth_positives + smooth_negatives

        losses = tf.nn.softmax_cross_entropy_with_logits(labels=y_true,
                                                         logits=y_pred,
                                                         name="xentropy")
        return losses

    return built_loss(inner_loss, weights, name, scope, collect, True)


def sigmoid_cross_entropy(weights=1.0, label_smoothing=0, name='SigmoidCrossEntropy', scope=None,
                          collect=True):
    """Computes Sigmoid cross entropy.(binary cross entropy):

    Computes sigmoid cross entropy between y_pred (logits) and y_true
    (labels).

    Measures the probability error in discrete classification tasks in which
    each class is independent and not mutually exclusive. For instance,
    one could perform multilabel classification where a picture can contain
    both an elephant and a dog at the same time.

    For brevity, let `x = logits`, `z = targets`.  The logistic loss is

      x - x * z + log(1 + exp(-x))

    To ensure stability and avoid overflow, the implementation uses

      max(x, 0) - x * z + log(1 + exp(-abs(x)))

    `y_pred` and `y_true` must have the same type and shape.

    Args:
        weights: Coefficients for the loss a `scalar`.
        label_smoothing: If greater than `0` then smooth the labels.
        scope: scope to add the op to.
        name: name of the op.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        if label_smoothing > 0:
            y_true = (y_true * (1 - label_smoothing) + 0.5 * label_smoothing)

        losses = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_true,
                                                         logits=y_pred,
                                                         name="xentropy")
        return losses

    return built_loss(inner_loss, weights, name, scope, collect, True)


def hinge_loss(weights=1.0, name='HingeLoss', scope=None, collect=True):
    """Hinge Loss.

    Args:
        weights: Coefficients for the loss a `scalar`.
        name: name of the op.
        scope: The scope for the operations performed in computing the loss.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        all_ones = array_ops.ones_like(y_true)
        y_true = math_ops.subtract(2 * y_true, all_ones)
        losses = tf.nn.relu(math_ops.subtract(all_ones, math_ops.multiply(y_true, y_pred)))
        return losses

    return built_loss(inner_loss, weights, name, scope, collect)


def cosine_distance(dim, weights=1.0, name='CosineDistance', scope=None, collect=True):
    """Adds a cosine-distance loss to the training procedure.

    Note that the function assumes that `predictions` and `labels` are already unit-normalized.

    WARNING: `weights` also supports dimensions of 1, but the broadcasting does
    not work as advertised, you'll wind up with weighted sum instead of weighted
    mean for any but the last dimension. This will be cleaned up soon, so please
    do not rely on the current behavior for anything but the shapes documented for
    `weights` below.

    Args:
        dim: The dimension along which the cosine distance is computed.
        weights: Coefficients for the loss a `scalar`.
        name: name of the op.
        scope: The scope for the operations performed in computing the loss.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        radial_diffs = math_ops.multiply(y_pred, y_true)
        losses = 1 - math_ops.reduce_sum(radial_diffs, axis=(dim,), keep_dims=True)
        return losses

    return built_loss(inner_loss, weights, name, scope, collect)


def kullback_leibler_divergence(weights=1.0, name='KullbackLeiberDivergence', scope=None,
                                collect=False):
    """Adds a Kullback leiber diverenge loss to the training procedure.

     Args:
        name: name of the op.
        scope: The scope for the operations performed in computing the loss.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        y_true = clip(y_true, EPSILON, 1)
        y_pred = clip(y_pred, EPSILON, 1)
        losses = tf.reduce_sum(input_tensor=y_true * tf.log(x=y_true / y_pred), axis=-1)
        return losses

    return built_loss(inner_loss, weights, name, scope, collect)


def poisson_loss(weights=1.0, name='PoissonLoss', scope=None, collect=False):
    """Adds a poisson loss to the training procedure.

     Args:
        name: name of the op.
        scope: The scope for the operations performed in computing the loss.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.
    """

    def inner_loss(y_true, y_pred):
        losses = tf.reduce_mean(input_tensor=y_pred - y_true * tf.log(x=y_pred + EPSILON), axis=-1)
        return losses

    return built_loss(inner_loss, weights, name, scope, collect)


LOSSES = OrderedDict([
    ('absolute_difference', absolute_difference),
    ('log_loss', log_loss),
    ('mean_squared_error', mean_squared_error),
    ('softmax_cross_entropy', softmax_cross_entropy),
    ('sigmoid_cross_entropy', sigmoid_cross_entropy),
    ('hinge_loss', hinge_loss),
    ('cosine_distance', cosine_distance),
    ('kullback_leibler_divergence', kullback_leibler_divergence),
    ('poisson_loss', poisson_loss),
    ('huber_loss', huber_loss),
    ('clipped_delta_loss', clipped_delta_loss),
])
