# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf


def create_learning_rate_decay_fn(decay_type, decay_steps, decay_rate, start_decay_at=0,
                                  stop_decay_at=1e9, min_learning_rate=None, staircase=False):
    """Creates a function that decays the learning rate.

    Args:
        decay_steps: How often to apply decay.
        decay_rate: A Python number. The decay rate.
        start_decay_at: Don't decay before this step
        stop_decay_at: Don't decay after this step
        min_learning_rate: Don't decay below this number
        decay_type: A decay function name defined in `tf.train`
        staircase: Whether to apply decay in a discrete staircase,
          as opposed to continuous, fashion.

    Returns:
        A function that takes (learning_rate, global_step) as inputs
        and returns the learning rate for the given step.
        Returns `None` if decay_type is empty or None.
    """
    if decay_type is None or decay_type == "":
        return None

    start_decay_at = tf.to_int32(start_decay_at)
    stop_decay_at = tf.to_int32(stop_decay_at)

    def decay_fn(learning_rate, global_step):
        """The computed learning rate decay function."""
        global_step = tf.to_int32(global_step)

        decay_type_fn = getattr(tf.train, decay_type)
        decayed_learning_rate = decay_type_fn(
            learning_rate=learning_rate,
            global_step=tf.minimum(global_step, stop_decay_at) - start_decay_at,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            staircase=staircase,
            name="decayed_learning_rate")

        final_lr = tf.train.piecewise_constant(
            x=global_step,
            boundaries=[start_decay_at],
            values=[learning_rate, decayed_learning_rate])

        if min_learning_rate:
            final_lr = tf.maximum(final_lr, min_learning_rate)

        return final_lr

    return decay_fn
