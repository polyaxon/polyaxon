# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.estimator.model_fn import ModeKeys
from tensorflow.python.training import moving_averages

from polyaxon.libs.template_module import BaseLayer
from polyaxon.libs.utils import get_shape, track
from polyaxon.variables import variable


class BatchNormalization(BaseLayer):
    def __init__(self, mode, beta=0.0, gamma=1.0, epsilon=1e-5, decay=0.9, stddev=0.002,
                 trainable=True, restore=True, name='BatchNormalization'):
        """Adds a Batch Normalization.

        Normalize activations of the previous layer at each batch.

        Args:
            beta: `float`. Default: 0.0.
            gamma: `float`. Default: 1.0.
            epsilon: `float`. Defalut: 1e-5.
            decay: `float`. Default: 0.9.
            stddev: `float`. Standard deviation for weights initialization.
            trainable: `bool`. If True, weights will be trainable.
            restore: `bool`. If True, this layer weights will be restored when
                loading a model.
            name: `str`. A name for this layer (optional).

        References:
            Batch Normalization: Accelerating Deep Network Training by Reducing
            Internal Covariate Shif. Sergey Ioffe, Christian Szegedy. 2015.

        Links:
            [http://arxiv.org/pdf/1502.03167v3.pdf](http://arxiv.org/pdf/1502.03167v3.pdf)
        """
        super(BatchNormalization, self).__init__(mode, name)
        self.beta = beta
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay = decay
        self.stddev = stddev
        self.trainable = trainable
        self.restore = restore

    def _build(self, incoming, *args, **kwargs):
        input_shape = get_shape(incoming)
        input_ndim = len(input_shape)
        gamma_init = tf.random_normal_initializer(mean=self.gamma, stddev=self.stddev)

        self._beta = variable(name='beta', shape=[input_shape[-1]],
                              initializer=tf.constant_initializer(self.beta),
                              trainable=self.trainable, restore=self.restore)
        self._gamma = variable(name='gamma', shape=[input_shape[-1]],
                               initializer=gamma_init, trainable=self.trainable,
                               restore=self.restore)

        track(self._beta, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        track(self._gamma, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        if not self.restore:
            track(tf.GraphKeys.EXCL_RESTORE_VARIABLES, self._beta)
            track(tf.GraphKeys.EXCL_RESTORE_VARIABLES, self._gamma)

        axis = list(range(input_ndim - 1))
        moving_mean = variable(name='moving_mean', shape=input_shape[-1:],
                               initializer=tf.zeros_initializer(), trainable=False,
                               restore=self.restore)
        moving_variance = variable(name='moving_variance', shape=input_shape[-1:],
                                   initializer=tf.constant_initializer(1.), trainable=False,
                                   restore=self.restore)

        def update_mean_var():
            mean, variance = tf.nn.moments(x=incoming, axes=axis)
            update_moving_mean = moving_averages.assign_moving_average(
                variable=moving_mean, value=mean, decay=self.decay, zero_debias=False)
            update_moving_variance = moving_averages.assign_moving_average(
                variable=moving_variance, value=variance, decay=self.decay, zero_debias=False)

            with tf.control_dependencies([update_moving_mean, update_moving_variance]):
                return tf.identity(mean), tf.identity(variance)

        # Retrieve variable managing training mode
        is_training = self.mode == ModeKeys.TRAIN
        mean, var = tf.cond(
            pred=is_training, fn1=update_mean_var, fn2=lambda: (moving_mean, moving_variance))

        incoming = tf.nn.batch_normalization(x=incoming, mean=mean, variance=var, offset=self._beta,
                                             scale=self._gamma, variance_epsilon=self.epsilon)
        incoming.set_shape(input_shape)

        track(incoming, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return incoming


class LocalResponseNormalization(BaseLayer):
    def __init__(self, mode, depth_radius=5, bias=1.0, alpha=0.0001, beta=0.75,
                 name='LocalResponseNormalization'):
        """ Local Response Normalization.

        Args:
            depth_radius: `int`. 0-D.  Half-width of the 1-D normalization window.
                Defaults to 5.
            bias: `float`. An offset (usually positive to avoid dividing by 0).
                Defaults to 1.0.
            alpha: `float`. A scale factor, usually positive. Defaults to 0.0001.
            beta: `float`. An exponent. Defaults to `0.5`.
            name: `str`. A name for this layer (optional).
        """
        super(LocalResponseNormalization, self).__init__(mode, name)
        self.depth_radius = depth_radius
        self.bias = bias
        self.alpha = alpha
        self.beta = beta

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            4-D Tensor Layer.
        Returns:
            4-D Tensor Layer. (Same dimension as input).
        """
        incoming = tf.nn.lrn( input=incoming, depth_radius=self.depth_radius, bias=self.bias,
                              alpha=self.alpha, beta=self.beta, name=self.name)
        track(incoming, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return incoming


class L2Normalization(BaseLayer):
    def __init__(self, mode, dim, epsilon=1e-12, name='l2Normalize'):
        """Adds an L2 Normalization.

        Normalizes along dimension `dim` using an L2 norm.

        For a 1-D tensor with `dim = 0`, computes
        ```python
        >>> output = x / sqrt(max(sum(x**2), epsilon))
        ```

        For `x` with more dimensions, independently normalizes each 1-D slice along
        dimension `dim`.

        Args:
            dim: `int`. Dimension along which to normalize.
            epsilon: `float`. A lower bound value for the norm. Will use
                `sqrt(epsilon)` as the divisor if `norm < sqrt(epsilon)`.
            name: `str`. A name for this layer (optional).
        """
        super(L2Normalization, self).__init__(mode, name)
        self.dim = dim
        self.epsilon = epsilon

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: 1-D tensor
        Returns:
            A `Tensor` with the same shape as `x`.
        """
        incoming = tf.convert_to_tensor(value=incoming, name='x')
        square_sum = tf.reduce_sum(input_tensor=tf.square(x=incoming), axis=[self.dim],
                                   keep_dims=True)
        x_inv_norm = tf.rsqrt(x=tf.maximum(x=square_sum, y=self.epsilon))
        incoming = tf.multiply(x=incoming, y=x_inv_norm, name=self.module_name)
        track(incoming, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return incoming


NORMALIZATIONS = {
    'batch_normalization': BatchNormalization,
    'local_response_normalization': LocalResponseNormalization,
    'l2_normalization': L2Normalization
}
