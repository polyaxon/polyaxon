# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import tensorflow as tf

from tensorflow.python.training.training_util import get_global_step

from polyaxon_schemas import optimizers

from polyaxon.libs.utils import track, get_arguments


def create_learning_rate_decay_fn(learning_rate, decay_type, decay_steps, decay_rate,
                                  start_decay_at=0, stop_decay_at=1e9, min_learning_rate=None,
                                  staircase=False, global_step=None):
    """Creates a function that decays the learning rate.

    Args:
        learning_rate: A Tensor or a floating point value. The learning rate to use.
        decay_steps: How often to apply decay.
        decay_rate: A Python number. The decay rate.
        start_decay_at: Don't decay before this step
        stop_decay_at: Don't decay after this step
        min_learning_rate: Don't decay below this number
        decay_type: A decay function name defined in `tf.train`
            possible Values: exponential_decay, inverse_time_decay, natural_exp_decay,
                             piecewise_constant, polynomial_decay.
        staircase: Whether to apply decay in a discrete staircase,
            as opposed to continuous, fashion.
        global_step: Scalar int `Tensor`, step counter for each update. If not supplied,
            it will be fetched from the default graph (see `tf.contrib.framework.get_global_step`
            for details). If it's not been created, no step will be incremented with each weight
            update. `learning_rate_decay_fn` requires `global_step`.

    Returns:
        A function that takes (learning_rate, global_step) as inputs
        and returns the learning rate for the given step.
        Returns `None` if decay_type is empty or None.
    """
    if decay_type is None or decay_type == "":
        return learning_rate

    start_decay_at = tf.to_int32(start_decay_at)
    stop_decay_at = tf.to_int32(stop_decay_at)

    def decay_fn(learning_rate, global_step):
        """The computed learning rate decay function."""
        global_step = tf.to_int32(global_step)
        decay_type_fn = getattr(tf.train, decay_type)
        kwargs = dict(
            learning_rate=learning_rate,
            global_step=tf.minimum(global_step, stop_decay_at) - start_decay_at,
            decay_steps=decay_steps,
            staircase=staircase,
            name="decayed_learning_rate"
        )
        decay_fn_args = get_arguments(decay_type_fn)
        if 'decay_rate' in decay_fn_args:
            kwargs['decay_rate'] = decay_rate
        if 'staircase' in decay_fn_args:
            kwargs['staircase'] = staircase

        decayed_learning_rate = decay_type_fn(**kwargs)

        final_lr = tf.train.piecewise_constant(
            x=global_step,
            boundaries=[start_decay_at],
            values=[learning_rate, decayed_learning_rate])

        if min_learning_rate:
            final_lr = tf.maximum(final_lr, min_learning_rate)

        return final_lr

    learning_rate = decay_fn(learning_rate, global_step or get_global_step())
    track(learning_rate, tf.GraphKeys.LEARNING_RATE)
    return learning_rate


def sgd(learning_rate=0.001, decay_type="", decay_rate=0., decay_steps=100, start_decay_at=0,
        stop_decay_at=tf.int32.max, min_learning_rate=1e-12, staircase=False, global_step=None,
        use_locking=False, name='SGD'):
    """Optimizer that implements the gradient descent algorithm.

    Args:
        learning_rate: A Tensor or a floating point value. The learning rate to use.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.GradientDescentOptimizer(
            learning_rate=_learning_rate, use_locking=use_locking, name=name)

    return optimizer


def momentum(learning_rate=0.001, momentum=0.9, decay_type="", decay_rate=0., decay_steps=10000,
             start_decay_at=0, stop_decay_at=tf.int32.max, min_learning_rate=1e-12, staircase=False,
             global_step=None, use_locking=False, name='Momentum'):
    # pylint: disable=redefined-outer-name
    """Optimizer that implements the Momentum.

    Momentum Optimizer accepts learning rate decay. When training a model,
    it is often recommended to lower the learning rate as the training
    progresses. The function returns the decayed learning rate.  It is
    computed as:

    ```python
    >>> decayed_learning_rate = learning_rate * decay_rate ^ (global_step / lr_decay_steps)
    ```
    Args:
        learning_rate: `float`. Learning rate.
        momentum: `float`. Momentum.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.MomentumOptimizer(
            learning_rate=_learning_rate, momentum=momentum, use_locking=use_locking, name=name)

    return optimizer


def nesterov(learning_rate=0.001, momentum=0.9, decay_type="", decay_rate=0., decay_steps=10000,
             start_decay_at=0, stop_decay_at=tf.int32.max, min_learning_rate=1e-12, staircase=False,
             use_locking=False, global_step=None, name='Momentum'):
    # pylint: disable=redefined-outer-name
    """Optimizer that implements the Nesterov.

    Same as Momentum optimizer but uses nestrov
    See [Sutskever et. al., 2013](http://jmlr.org/proceedings/papers/v28/sutskever13.pdf)

    ```python
    >>> decayed_learning_rate = learning_rate * decay_rate ^ (global_step / lr_decay_steps)
    ```
    Args:
        learning_rate: `float`. Learning rate.
        momentum: `float`. Momentum.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.MomentumOptimizer(
            learning_rate=_learning_rate, momentum=momentum, use_locking=use_locking, name=name,
            use_nesterov=True)

    return optimizer


def rmsprop(learning_rate=0.001, decay=0.9, momentum=0.0, epsilon=1e-10, decay_type="",
            decay_rate=0., decay_steps=10000, start_decay_at=0, stop_decay_at=tf.int32.max,
            min_learning_rate=1e-12, staircase=False, global_step=None,
            use_locking=False, name='RMSProp'):
    # pylint: disable=redefined-outer-name
    """Optimizer that implements the RMSprop.

    Maintain a moving (discounted) average of the square of gradients.
    Divide gradient by the root of this average.

    Args:
        learning_rate: `float`. learning rate.
        decay: `float`. Discounting factor for the history/coming gradient.
        momentum: `float`. Momentum.
        epsilon: `float`. Small value to avoid zero denominator.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.RMSPropOptimizer(
            learning_rate=_learning_rate, decay=decay, momentum=momentum, epsilon=epsilon,
            use_locking=use_locking, name=name)

    return optimizer


def adam(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, decay_type="",
         decay_rate=0., decay_steps=10000, start_decay_at=0, stop_decay_at=tf.int32.max,
         min_learning_rate=1e-12, staircase=False, global_step=None,
         use_locking=False, name='Adam'):
    """Optimizer that implements the Adam.

    The default value of 1e-8 for epsilon might not be a good default in
    general. For example, when training an Inception network on ImageNet a
    current good choice is 1.0 or 0.1.

    Args:
        learning_rate: `float`. learning rate.
        beta1: `float`. The exponential decay rate for the 1st moment estimates.
        beta2: `float`. The exponential decay rate for the 2nd moment estimates.
        epsilon: `float`. A small constant for numerical stability.
        epsilon: `float`. Small value to avoid zero denominator.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.AdamOptimizer(
            learning_rate=_learning_rate, beta1=beta1, beta2=beta2, epsilon=epsilon,
            use_locking=use_locking, name=name)

    return optimizer


def adagrad(learning_rate=0.001, initial_accumulator_value=0.1, decay_type="",
            decay_rate=0., decay_steps=10000, start_decay_at=0, stop_decay_at=tf.int32.max,
            min_learning_rate=1e-12, staircase=False, global_step=None,
            use_locking=False, name='AdaGrad'):
    """Optimizer that implements AdaGrad.

    Args:
        learning_rate: `float`. Learning rate.
        initial_accumulator_value: `float`. Starting value for the
            accumulators, must be positive.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.AdagradOptimizer(
            learning_rate=_learning_rate, initial_accumulator_value=initial_accumulator_value,
            use_locking=use_locking, name=name)

    return optimizer


def ftrl(learning_rate=3.0, learning_rate_power=-0.5, initial_accumulator_value=0.1,
         l1_regularization_strength=0.0, l2_regularization_strength=0.0, decay_type="",
         decay_rate=0., decay_steps=10000, start_decay_at=0, stop_decay_at=tf.int32.max,
         min_learning_rate=1e-12, staircase=False, global_step=None,
         use_locking=False, name='Ftrl'):
    """Optimizer that implements Ftrl Proximal.

    The Ftrl-proximal algorithm, abbreviated for Follow-the-regularized-leader,
    is described in the paper below.

    It can give a good performance vs. sparsity tradeoff.

    Ftrl-proximal uses its own global base learning rate and can behave like
    Adagrad with `learning_rate_power=-0.5`, or like gradient descent with
    `learning_rate_power=0.0`.

    Args:
        learning_rate: `float`. Learning rate.
        learning_rate_power: `float`. Must be less or equal to zero.
        initial_accumulator_value: `float`. The starting value for accumulators.
            Only positive values are allowed.
        l1_regularization_strength: `float`. Must be less or equal to zero.
        l2_regularization_strength: `float`. Must be less or equal to zero.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients..
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.FtrlOptimizer(
            learning_rate=_learning_rate, learning_rate_power=learning_rate_power,
            initial_accumulator_value=initial_accumulator_value,
            l1_regularization_strength=l1_regularization_strength,
            l2_regularization_strength=l2_regularization_strength,
            use_locking=use_locking, name=name)

    return optimizer


def adadelta(learning_rate=0.001, rho=0.1, epsilon=1e-08, decay_type="",
             decay_rate=0., decay_steps=10000, start_decay_at=0, stop_decay_at=tf.int32.max,
             min_learning_rate=1e-12, staircase=False, global_step=None,
             use_locking=False, name='AdaDelta'):
    """Optimizer that implements AdaDelta.

    Args:
        learning_rate: A `Tensor` or a floating point value. The learning rate.
        rho: A `Tensor` or a floating point value. The decay rate.
        epsilon: A `Tensor` or a floating point value.  A constant epsilon used to better
            conditioning the grad update.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        _learning_rate = create_learning_rate_decay_fn(
            learning_rate=learning_rate,
            decay_type=decay_type,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            start_decay_at=start_decay_at,
            stop_decay_at=stop_decay_at,
            min_learning_rate=min_learning_rate,
            staircase=staircase,
            global_step=global_step)

        return tf.train.AdadeltaOptimizer(learning_rate=_learning_rate, rho=rho, epsilon=epsilon,
                                          use_locking=use_locking, name=name)

    return optimizer


OPTIMIZERS = OrderedDict([
    (optimizers.AdadeltaConfig.IDENTIFIER, adadelta),
    (optimizers.AdagradConfig.IDENTIFIER, adagrad),
    (optimizers.AdamConfig.IDENTIFIER, adam),
    (optimizers.FtrlConfig.IDENTIFIER, ftrl),
    (optimizers.MomentumConfig.IDENTIFIER, momentum),
    (optimizers.NestrovConfig.IDENTIFIER, nesterov),
    (optimizers.RMSPropConfig.IDENTIFIER, rmsprop),
    (optimizers.SGDConfig.IDENTIFIER, sgd),
])
