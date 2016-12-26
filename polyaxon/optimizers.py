# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.libs.utils import track


def sgd(learning_rate=0.001, lr_decay=0., decay_step=100, staircase=False, use_locking=False,
        global_step=None, name='SGD'):
    """ Optimizer that implements the gradient descent algorithm.

    Args:
        learning_rate: A Tensor or a floating point value. The learning rate to use.
        lr_decay: `float`. The learning rate decay to apply.
        decay_step: `int`. Apply decay every provided steps.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        use_locking: If True use locks for update operations.
        global_step: Scalar int `Tensor`, step counter for each update. If not
        supplied, it will be fetched from the default graph (see
            `tf.contrib.framework.get_global_step` for details). If it's
            not been created, no step will be incremented with each weight
            update. `learning_rate_decay_fn` requires `global_step`.
        name: Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        lr = learning_rate
        if lr_decay > 0:
            step_tensor = global_step or tf.contrib.framework.get_global_step()
            lr = tf.train.exponential_decay(learning_rate=learning_rate, global_step=step_tensor,
                                            decay_steps=decay_step,
                                            decay_rate=lr_decay, staircase=staircase)
            track(lr, tf.GraphKeys.LEARNING_RATE_VARS)

        return tf.train.GradientDescentOptimizer(
            learning_rate=lr, use_locking=use_locking, name=name)

    return optimizer


def rmsprop(learning_rate=0.001, decay=0.9, momentum=0.0, epsilon=1e-10, use_locking=False,
            name='RMSProp'):
    """ Optimizer that implements the RMSprop.

    Maintain a moving (discounted) average of the square of gradients.
    Divide gradient by the root of this average.

    Args:
        learning_rate: `float`. learning rate.
        decay: `float`. Discounting factor for the history/coming gradient.
        momentum: `float`. Momentum.
        epsilon: `float`. Small value to avoid zero denominator.
        use_locking: `bool`. If True use locks for update operation.
        name: Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        return tf.train.RMSPropOptimizer(
            learning_rate=learning_rate, decay=decay, momentum=momentum, epsilon=epsilon,
            use_locking=use_locking, name=name)

    return optimizer


def adam(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, use_locking=False, name='Adam'):
    """ Optimizer that implements the Adam.

    The default value of 1e-8 for epsilon might not be a good default in
    general. For example, when training an Inception network on ImageNet a
    current good choice is 1.0 or 0.1.

    Args:
        learning_rate: `float`. learning rate.
        beta1: `float`. The exponential decay rate for the 1st moment estimates.
        beta2: `float`. The exponential decay rate for the 2nd moment estimates.
        epsilon: `float`. A small constant for numerical stability.
        use_locking: `bool`. If True use locks for update operation.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """
    def optimizer():
        return tf.train.AdamOptimizer(
            learning_rate=learning_rate, beta1=beta1, beta2=beta2, epsilon=epsilon,
            use_locking=use_locking, name=name)

    return optimizer


def momentum(learning_rate=0.001, momentum=0.9, lr_decay=0., decay_step=100, staircase=False,
             use_locking=False, global_step=None, name='Momentum'):
    """ Optimizer that implements the Momentum.

    Momentum Optimizer accepts learning rate decay. When training a model,
    it is often recommended to lower the learning rate as the training
    progresses. The function returns the decayed learning rate.  It is
    computed as:

    ```python
    decayed_learning_rate = learning_rate *
                          decay_rate ^ (global_step / decay_steps)
    ```
    Args:
        learning_rate: `float`. Learning rate.
        momentum: `float`. Momentum.
        lr_decay: `float`. The learning rate decay to apply.
        decay_step: `int`. Apply decay every provided steps.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        use_locking: `bool`. If True use locks for update operation.
        global_step: Scalar int `Tensor`, step counter for each update. If not
        supplied, it will be fetched from the default graph (see
            `tf.contrib.framework.get_global_step` for details). If it's
            not been created, no step will be incremented with each weight
            update. `learning_rate_decay_fn` requires `global_step`.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        lr = learning_rate
        if lr_decay > 0:
            step_tensor = global_step or tf.train.get_global_step()
            lr = tf.train.exponential_decay(learning_rate=learning_rate, global_step=step_tensor,
                                            decay_steps=decay_step,
                                            decay_rate=lr_decay, staircase=staircase)
            track(lr, tf.GraphKeys.LEARNING_RATE_VARS)

        return tf.train.MomentumOptimizer(
            learning_rate=lr, momentum=momentum, use_locking=use_locking, name=name)

    return optimizer


def adagrad(learning_rate=0.001, initial_accumulator_value=0.1, use_locking=False, name='AdaGrad'):
    """ Optimizer that implements AdaGrad.

    Args:
        learning_rate: `float`. Learning rate.
        initial_accumulator_value: `float`. Starting value for the
            accumulators, must be positive
        use_locking: `bool`. If True use locks for update operation.
        name: `str`. Optional name prefix for the operations created when applying gradients.
    """

    def optimizer():
        return tf.train.AdagradOptimizer(
            learning_rate=learning_rate, initial_accumulator_value=initial_accumulator_value,
            use_locking=use_locking, name=name)

    return optimizer


def ftrl(learning_rate=3.0, learning_rate_power=-0.5, initial_accumulator_value=0.1,
         l1_regularization_strength=0.0, l2_regularization_strength=0.0, use_locking=False,
         name='Ftrl'):
    """ Optimizer that implements Ftrl Proximal.

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
        use_locking: bool`. If True use locks for update operation.
        name: `str`. Optional name prefix for the operations created when applying gradients..
    """

    def optimizer():
        with tf.device('/cpu:0'):
            return tf.train.FtrlOptimizer(
                learning_rate=learning_rate, learning_rate_power=learning_rate_power,
                initial_accumulator_value=initial_accumulator_value,
                l1_regularization_strength=l1_regularization_strength,
                l2_regularization_strength=l2_regularization_strength,
                use_locking=use_locking, name=name)

    return optimizer


def adadelta(learning_rate=0.001, rho=0.1, epsilon=1e-08, use_locking=False, name='AdaDelta'):
    """ Optimizer that implements AdaDelta.

    Args:
        learning_rate: A `Tensor` or a floating point value. The learning rate.
        rho: A `Tensor` or a floating point value. The decay rate.
        epsilon: A `Tensor` or a floating point value.  A constant epsilon used to better
            conditioning the grad update.
        use_locking: If `True` use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.
    """
    def optimizer():
        return tf.train.AdadeltaOptimizer(learning_rate=learning_rate, rho=rho, epsilon=epsilon,
                                          use_locking=use_locking, name=name)

    return optimizer


OPTIMIZERS = {
    'Adagrad': adagrad,
    'Adam': adam,
    'Ftrl': ftrl,
    'Momentum': momentum,
    'RMSProp': rmsprop,
    'SGD': sgd,
}
