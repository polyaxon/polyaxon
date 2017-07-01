# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.python.framework import constant_op
from tensorflow.python.framework import ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops

from polyaxon.libs.utils import get_name_scope


def exponential_decay(exploration_rate, timestep, decay_steps, decay_rate, staircase=False,
                      name=None):
    """Applies exponential decay to the exploration rate.

    When training a model, it is often recommended to lower the exploration rate as
    the training progresses.  This function applies an exponential decay function
    to a provided initial exploration rate.  It requires a `timestep` value to
    compute the decayed exploration rate.  You can just pass a TensorFlow variable
    that you increment at each training step.
    
    The function returns the decayed exploration rate.  It is computed as:

    ```python
    >>> decayed_exploration_rate = exploration_rate * decay_rate ^ (timestep / decay_steps)
    ```

    If the argument `staircase` is `True`, then `timestep / decay_steps` is an
    integer division and the decayed exploration rate follows a staircase function.

    Example: decay every 100000 steps with a base of 0.96:

    ```python
    >>> timestep = tf.Variable(0, trainable=False)
    >>> starter_exploration_rate = 0.1
    >>> exploration_rate = tf.train.exponential_decay(starter_exploration_rate, timestep,
    ...                                               100000, 0.96, staircase=True)
    >>> # Passing timestep to minimize() will increment it at each step.
    >>> learning_step = (
    ... tf.train.GradientDescentOptimizer(exploration_rate)
    ...   .minimize(...my loss..., timestep=timestep)
    ... )
    ```

    Args:
        exploration_rate: A scalar `float32` or `float64` `Tensor` or a Python number.  
            The initial exploration rate.
        timestep: A scalar `int32` or `int64` `Tensor` or a Python number.
            Global step to use for the decay computation.  Must not be negative.
        decay_steps: A scalar `int32` or `int64` `Tensor` or a Python number.
            Must be positive.  See the decay computation above.
        decay_rate: A Python number.  The decay rate.
        staircase: Boolean.  If `True` decay the exploration rate at discrete intervals.
        name: String.  Optional name of the operation.  Defaults to 'ExplorationExponentialDecay'.

    Returns:
        A scalar `Tensor` of the same type as `exploration_rate`. The decayed exploration rate.

    Raises:
        ValueError: if `timestep` is not supplied.
    """
    if timestep is None:
        raise ValueError("timestep is required for exponential_decay.")
    with get_name_scope(name=name, scope="ExponentialDecay",
                        values=[exploration_rate, timestep, decay_steps, decay_rate]) as name:
        exploration_rate = ops.convert_to_tensor(exploration_rate, name="exploration_rate")
        dtype = exploration_rate.dtype
        timestep = math_ops.cast(timestep, dtype)
        decay_steps = math_ops.cast(decay_steps, dtype)
        decay_rate = math_ops.cast(decay_rate, dtype)
        p = timestep / decay_steps
        if staircase:
            p = math_ops.floor(p)
        return math_ops.multiply(exploration_rate, math_ops.pow(decay_rate, p), name=name)


def piecewise_constant(x, boundaries, values, name=None):
    """Piecewise constant from boundaries and interval values.

    Example: use a exploration rate that's 1.0 for the first 100000 steps, 0.5 for steps
    100001 to 110000, and 0.1 for any additional steps.

    ```python
    timestep = tf.Variable(0, trainable=False)
    boundaries = [100000, 110000]
    values = [1.0, 0.5, 0.1]
    exploration_rate = tf.train.piecewise_constant(timestep, boundaries, values)

    # Later, whenever we perform an optimization step, we increment timestep.
    ```

    Args:
        x: A 0-D scalar `Tensor`. Must be one of the following types: `float32`,
            `float64`, `uint8`, `int8`, `int16`, `int32`, `int64`.
        boundaries: A list of `Tensor`s or `int`s or `float`s with strictly
            increasing entries, and with all elements having the same type as `x`.
        values: A list of `Tensor`s or float`s or `int`s that specifies the values
            for the intervals defined by `boundaries`. It should have one more element
            than `boundaries`, and all elements should have the same type.
        name: A string. Optional name of the operation. Defaults to 'PiecewiseConstant'.

    Returns:
        A 0-D Tensor. Its value is `values[0]` when `x <= boundaries[0]`,
            `values[1]` when `x > boundaries[0]` and `x <= boundaries[1]`, ...,
            and values[-1] when `x > boundaries[-1]`.

    Raises:
        ValueError: if types of `x` and `buondaries` do not match, or types of all
        `values` do not match.
    """
    with get_name_scope(name=name, scope="PiecewiseConstant",
                        values=[x, boundaries, values, name]) as name:
        x = ops.convert_to_tensor(x)
        # Avoid explicit conversion to x's dtype. This could result in faulty
        # comparisons, for example if floats are converted to integers.
        boundaries = ops.convert_n_to_tensor(boundaries)
        for b in boundaries:
            if b.dtype != x.dtype:
                raise ValueError(
                    "Boundaries (%s) must have the same dtype as x (%s)." % (
                        b.dtype, x.dtype))
        values = ops.convert_n_to_tensor(values)
        for v in values[1:]:
            if v.dtype != values[0].dtype:
                raise ValueError(
                    "Values must have elements all with the same dtype (%s vs %s)." % (
                        values[0].dtype, v.dtype))

        pred_fn_pairs = {}
        pred_fn_pairs[x <= boundaries[0]] = lambda: values[0]
        pred_fn_pairs[x > boundaries[-1]] = lambda: values[-1]
        for low, high, v in zip(boundaries[:-1], boundaries[1:], values[1:-1]):
            # Need to bind v here; can do this with lambda v=v: ...
            pred = (x > low) & (x <= high)
            pred_fn_pairs[pred] = lambda v=v: v

        # The default isn't needed here because our conditions are mutually
        # exclusive and exhaustive, but tf.case requires it.
        default = lambda: values[0]
        return control_flow_ops.case(pred_fn_pairs, default, exclusive=True)


def polynomial_decay(exploration_rate, timestep, decay_steps,
                     end_exploration_rate=0.0001, power=1.0,
                     cycle=False, name=None):
    """Applies a polynomial decay to the exploration rate.

    It is commonly observed that a monotonically decreasing exploration rate, whose
    degree of change is carefully chosen, results in a better performing model.
    This function applies a polynomial decay function to a provided initial
    `exploration_rate` to reach an `end_exploration_rate` in the given `decay_steps`.

    It requires a `timestep` value to compute the decayed exploration rate.  You
    can just pass a TensorFlow variable that you increment at each training step.

    The function returns the decayed exploration rate.  It is computed as:

    ```python
    >>> timestep = min(timestep, decay_steps)
    >>> decayed_exploration_rate = (exploration_rate - end_exploration_rate) *
    ...                            (1 - timestep / decay_steps) ^ (power) + end_exploration_rate
    ```

    If `cycle` is True then a multiple of `decay_steps` is used, the first one
    that is bigger than `timesteps`.

    ```python
    >>> decay_steps = decay_steps * ceil(timestep / decay_steps)
    >>> decayed_exploration_rate = (exploration_rate - end_exploration_rate) *
    ...                            (1 - timestep / decay_steps) ^ (power) +
    ...                            end_exploration_rate

    ```

    Example: decay from 0.1 to 0.01 in 10000 steps using sqrt (i.e. power=0.5):

    ```python
    >>> timestep = tf.Variable(0, trainable=False)
    >>> starter_exploration_rate = 0.1
    >>> end_exploration_rate = 0.01
    >>> decay_steps = 10000
    >>> exploration_rate = tf.train.polynomial_decay(starter_exploration_rate, timestep,
    ...                                              decay_steps, end_exploration_rate, power=0.5)
    >>> # Passing timestep to minimize() will increment it at each step.
    >>> learning_step = (
    ...     tf.train.GradientDescentOptimizer(exploration_rate)
    ...     .minimize(...my loss..., timestep=timestep)
    ... )
    ```

    Args:
        exploration_rate: A scalar `float32` or `float64` `Tensor` or a
            Python number.  The initial exploration rate.
        timestep: A scalar `int32` or `int64` `Tensor` or a Python number.
            Global step to use for the decay computation.  Must not be negative.
        decay_steps: A scalar `int32` or `int64` `Tensor` or a Python number.
            Must be positive.  See the decay computation above.
        end_exploration_rate: A scalar `float32` or `float64` `Tensor` or a
            Python number.  The minimal end exploration rate.
        power: A scalar `float32` or `float64` `Tensor` or a
            Python number.  The power of the polynomial. Defaults to linear, 1.0.
        cycle: A boolean, whether or not it should cycle beyond decay_steps.
        name: String.  Optional name of the operation. Defaults to
            'PolynomialDecay'.

    Returns:
        A scalar `Tensor` of the same type as `exploration_rate`.  The decayed exploration rate.

    Raises:
        ValueError: if `timestep` is not supplied.
    """
    if timestep is None:
        raise ValueError("timestep is required for polynomial_decay.")
    with get_name_scope(name=name, scope="PolynomialDecay",
                        values=[exploration_rate, timestep,
                                decay_steps, end_exploration_rate, power]) as name:
        exploration_rate = ops.convert_to_tensor(exploration_rate, name="exploration_rate")
        dtype = exploration_rate.dtype
        timestep = math_ops.cast(timestep, dtype)
        decay_steps = math_ops.cast(decay_steps, dtype)
        end_exploration_rate = math_ops.cast(end_exploration_rate, dtype)
        power = math_ops.cast(power, dtype)
        if cycle:
            # Find the first multiple of decay_steps that is bigger than timestep.
            decay_steps = math_ops.multiply(decay_steps,
                                            math_ops.ceil(timestep / decay_steps))
        else:
            # Make sure that the timestep used is not bigger than decay_steps.
            timestep = math_ops.minimum(timestep, decay_steps)

        p = math_ops.div(timestep, decay_steps)
        return math_ops.add(math_ops.multiply(exploration_rate - end_exploration_rate,
                                              math_ops.pow(1 - p, power)),
                            end_exploration_rate, name=name)


def natural_exp_decay(exploration_rate, timestep, decay_steps, decay_rate,
                      staircase=False, name=None):
    """Applies natural exponential decay to the initial exploration rate.

    When training a model, it is often recommended to lower the exploration rate as
    the training progresses.  This function applies an exponential decay function
    to a provided initial exploration rate.  It requires an `timestep` value to
    compute the decayed exploration rate.  You can just pass a TensorFlow variable
    that you increment at each training step.

    The function returns the decayed exploration rate.  It is computed as:

    ```python
    >>> decayed_exploration_rate = exploration_rate * exp(-decay_rate * timestep)
    ```

    Example: decay exponentially with a base of 0.96:

    ```python
    >>> timestep = tf.Variable(0, trainable=False)
    >>> exploration_rate = 0.1
    >>> k = 0.5
    >>> exploration_rate = tf.train.exponential_time_decay(exploration_rate, timestep, k)

    >>> # Passing timestep to minimize() will increment it at each step.
    >>> learning_step = (
    ...     tf.train.GradientDescentOptimizer(exploration_rate)
    ...     .minimize(...my loss..., timestep=timestep)
    ... )
    ```

    Args:
        exploration_rate: A scalar `float32` or `float64` `Tensor` or a
            Python number.  The initial exploration rate.
        timestep: A Python number.
            Global step to use for the decay computation.  Must not be negative.
        decay_steps: How often to apply decay.
        decay_rate: A Python number.  The decay rate.
        staircase: Whether to apply decay in a discrete staircase,
            as opposed to continuous, fashion.
        name: String.  Optional name of the operation.  Defaults to 'ExponentialTimeDecay'.

    Returns:
        A scalar `Tensor` of the same type as `exploration_rate`.  The decayed exploration rate.

    Raises:
        ValueError: if `timestep` is not supplied.
    """
    if timestep is None:
        raise ValueError("timestep is required for natural_exp_decay.")
    with get_name_scope(name=name, scope="NaturalExpDecay",
                        values=[exploration_rate, timestep, decay_rate]) as name:
        exploration_rate = ops.convert_to_tensor(exploration_rate, name="exploration_rate")
        dtype = exploration_rate.dtype
        timestep = math_ops.cast(timestep, dtype)
        decay_steps = math_ops.cast(decay_steps, dtype)
        decay_rate = math_ops.cast(decay_rate, dtype)
        p = timestep / decay_steps
        if staircase:
            p = math_ops.floor(p)
        exponent = math_ops.exp(math_ops.multiply(math_ops.negative(decay_rate), p))
        return math_ops.multiply(exploration_rate, exponent, name=name)


def inverse_time_decay(exploration_rate, timestep, decay_steps, decay_rate,
                       staircase=False, name=None):
    """Applies inverse time decay to the initial exploration rate.

    When training a model, it is often recommended to lower the exploration rate as
    the training progresses.  This function applies an inverse decay function
    to a provided initial exploration rate.  It requires an `timestep` value to
    compute the decayed exploration rate.  You can just pass a TensorFlow variable
    that you increment at each training step.

    The function returns the decayed exploration rate.  It is computed as:

    ```python
    >>> decayed_exploration_rate = exploration_rate / (1 + decay_rate * t)
    ```

    Example: decay 1/t with a rate of 0.5:

    ```python
    >>> timestep = tf.Variable(0, trainable=False)
    >>> exploration_rate = 0.1
    >>> k = 0.5
    >>> exploration_rate = tf.train.inverse_time_decay(exploration_rate, timestep, k)

    >>> # Passing timestep to minimize() will increment it at each step.
    >>> learning_step = (
    ...     tf.train.GradientDescentOptimizer(exploration_rate)
    ...     .minimize(...my loss..., timestep=timestep)
    ... )
    ```

    Args:
        exploration_rate: A scalar `float32` or `float64` `Tensor` or a Python number.
            The initial exploration rate.
        timestep: A Python number.
            Global step to use for the decay computation.  Must not be negative.
        decay_steps: How often to apply decay.
        decay_rate: A Python number.  The decay rate.
        staircase: Whether to apply decay in a discrete staircase, as opposed to
            continuous, fashion.
        name: String.  Optional name of the operation.  Defaults to 'InverseTimeDecay'.

    Returns:
        A scalar `Tensor` of the same type as `exploration_rate`.  The decayed exploration rate.

    Raises:
        ValueError: if `timestep` is not supplied.
    """
    if timestep is None:
        raise ValueError("timestep is required for inverse_time_decay.")
    with ops.name_scope(name, "InverseTimeDecay",
                        [exploration_rate, timestep, decay_rate]) as name:
        exploration_rate = ops.convert_to_tensor(exploration_rate, name="exploration_rate")
        dtype = exploration_rate.dtype
        timestep = math_ops.cast(timestep, dtype)
        decay_steps = math_ops.cast(decay_steps, dtype)
        decay_rate = math_ops.cast(decay_rate, dtype)
        p = timestep / decay_steps
        if staircase:
            p = math_ops.floor(p)
        const = math_ops.cast(constant_op.constant(1), exploration_rate.dtype)
        denom = math_ops.add(const, math_ops.multiply(decay_rate, p))
        return math_ops.div(exploration_rate, denom, name=name)
