# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from math import ceil
from six.moves import xrange

import numpy as np
import tensorflow as tf

from polyaxon.layers.normalizations import BatchNormalization
from polyaxon.libs import getters
from polyaxon.libs.template_module import BaseLayer
from polyaxon.libs.utils import (
    get_shape,
    int_or_tuple,
    int_or_tuple_3d,
    track,
    validate_filter_size,
    validate_filter_size_3d,
    validate_padding,
    validate_dtype)
from polyaxon.variables import variable


class Conv2d(BaseLayer):
    """Adds a 2D convolution layer.

    This operation creates a variable called 'w', representing the convolutional kernel,
    that is convolved with the input. A second variable called 'b' is added to the result of
    the convolution operation.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: `int` or `list of int`. Size of filters.
        strides: 'int` or list of `int`. Strides of conv operation.
            Default: [1 1 1 1].
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`) or None.
            Default: 'linear'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Conv2D'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        b: `Variable`. Variable representing biases.
    """
    def __init__(self, mode, num_filter, filter_size, strides=1, padding='SAME',
                 activation='linear', bias=True, weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name='Conv2D'):
        super(Conv2d, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            4-D Tensor [batch, height, width, in_channels].
        Returns:
            4-D Tensor [batch, new height, new width, num_filter].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'
        filter_size = validate_filter_size(self.filter_size, input_shape[-1], self.num_filter)
        strides = int_or_tuple(self.strides)
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        self._w = variable('w', shape=filter_size, regularizer=regularizer,
                           initializer=getters.get_initializer(self.weights_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        inference = tf.nn.conv2d(input=incoming, filter=self._w, strides=strides, padding=padding)

        self._b = None
        if self.bias:
            self._b = variable(name='b', shape=self.num_filter,
                               initializer=getters.get_initializer(self.bias_init),
                               trainable=self.trainable, restore=self.restore)
            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            inference = tf.nn.bias_add(value=inference, bias=self._b)

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Conv2dTranspose(BaseLayer):
    """Adds a Convolution 2D Transpose.

    This operation is sometimes called "deconvolution" after (Deconvolutional
    Networks)[http://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf], but is
    actually the transpose (gradient) of `conv2d` rather than an actual
    deconvolution.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: `int` or `list of int`. Size of filters.
        output_shape: `list of int`. Dimensions of the output tensor.
            Can optionally include the number of conv filters.
            [new height, new width, num_filter] or [new height, new width].
        strides: `int` or list of `int`. Strides of conv operation.
            Default: [1 1 1 1].
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Conv2DTranspose'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        b: `Variable`. Variable representing biases.
    """
    def __init__(self, mode, num_filter, filter_size, output_shape, strides=1, padding='SAME',
                 activation='linear', bias=True, weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name='Conv2DTranspose'):
        super(Conv2dTranspose, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.output_shape = output_shape
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            4-D Tensor [batch, height, width, in_channels].

        Returns:
            4-D Tensor [batch, new height, new width, num_filter].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'
        filter_size = validate_filter_size(self.filter_size, self.num_filter, input_shape[-1])
        strides = int_or_tuple(self.strides)
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        self._w = variable('w', shape=filter_size, regularizer=regularizer,
                           initializer=getters.get_initializer(self.weights_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Determine the complete shape of the output tensor.
        batch_size = tf.gather(params=tf.shape(input=incoming), indices=tf.constant([0]))
        output_shape = self.output_shape
        if len(output_shape) == 2:
            output_shape = self.output_shape + [self.num_filter]
        elif len(output_shape) != 3:
            raise Exception('output_shape length error: {}, '
                            'only a length of 2 or 3 is supported.'.format(len(output_shape)))

        complete_out_shape = tf.concat(axis=0, values=[batch_size, tf.constant(value=output_shape)])
        inference = tf.nn.conv2d_transpose(value=incoming, filter=self._w,
                                           output_shape=complete_out_shape,
                                           strides=strides, padding=padding)
        # Reshape tensor so its shape is correct.
        inference.set_shape([None] + output_shape)

        self._b = None
        if self.bias:
            self._b = variable('b', shape=self.num_filter,
                               initializer=getters.get_initializer(self.bias_init),
                               trainable=self.trainable, restore=self.restore)

            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            inference = tf.nn.bias_add(value=inference, bias=self._b)

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Pool2dMixin(object):
    """A Mixin to add pooling 2d operation."""

    def _pool2d(self, incoming, fct):
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'

        kernel = int_or_tuple(self.kernel_size)
        strides = int_or_tuple(self.strides) if self.strides else kernel
        padding = validate_padding(self.padding)

        inference = fct(incoming, kernel, strides, padding)
        track(inference, tf.GraphKeys.ACTIVATIONS)
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class MaxPool2d(BaseLayer, Pool2dMixin):
    """Adds Max Pooling 2D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: 'int` or `list of int`. Pooling kernel size.
        strides: 'int` or `list of int`. Strides of conv operation.
            Default: SAME as kernel_size.
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        name: A name for this layer (optional). Default: 'MaxPool2D'.
    """
    def __init__(self, mode, kernel_size, strides=None, padding='SAME', name='MaxPool2D'):
        super(MaxPool2d, self).__init__(mode, name)
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            4-D Tensor [batch, height, width, in_channels].

        Returns:
            4-D Tensor [batch, pooled height, pooled width, in_channels].
        """
        return self._pool2d(incoming, tf.nn.max_pool)


class AvgPool2d(BaseLayer, Pool2dMixin):
    """Adds Average Pooling 2D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: 'int` or `list of int`. Pooling kernel size.
        strides: 'int` or `list of int`. Strides of conv operation.
            Default: SAME as kernel_size.
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        name: A name for this layer (optional). Default: 'AvgPool2D'.
    """
    def __init__(self, mode, kernel_size, strides=None, padding='SAME', name='AvgPool2D'):
        super(AvgPool2d, self).__init__(mode, name)
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            4-D Tensor [batch, height, width, in_channels].

        Returns:
            4-D Tensor [batch, pooled height, pooled width, in_channels].
        """
        return self._pool2d(incoming, tf.nn.avg_pool)


class Upsample2d(BaseLayer):
    """Adds UpSample 2D operation.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: 'int` or `list of int`. Upsampling kernel size.
        name: A name for this layer (optional). Default: 'UpSample2D'.
    """
    def __init__(self, mode, kernel_size, name='UpSample2D'):
        super(Upsample2d, self).__init__(mode, name)
        self.kernel_size = kernel_size

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 4-D Tensor [batch, height, width, in_channels] to upsample.

        Returns:
            4-D Tensor [batch, pooled height, pooled width, in_channels].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'
        kernel = int_or_tuple(self.kernel_size)

        inference = tf.image.resize_nearest_neighbor(
            images=incoming, size=input_shape[1:3] * tf.constant(kernel[1:3]))
        inference.set_shape((None, input_shape[1] * kernel[1], input_shape[2] * kernel[2], None))
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Upscore(BaseLayer):
    """Adds an Upscore layer.

    This implements the upscore layer as used in
    (Fully Convolutional Networks)[http://arxiv.org/abs/1411.4038].
    The upscore layer is initialized as bilinear upsampling filter.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_classes: `int`. Number of output feature maps.
        shape: `list of int`. Dimension of the output map
            [batch_size, new height, new width]. For convinience four values
             are allows [batch_size, new height, new width, X], where X
             is ignored.
        kernel_size: 'int` or `list of int`. Upsampling kernel size.
        strides: 'int` or `list of int`. Strides of conv operation.
            Default: [1 2 2 1].
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Upscore'.

    Links:
        (Fully Convolutional Networks)[http://arxiv.org/abs/1411.4038]
    """
    def __init__(self, mode, num_classes, shape=None, kernel_size=4, strides=2, trainable=True,
                 restore=True, name='Upscore'):
        super(Upscore, self).__init__(mode, name)
        self.num_classes = num_classes
        self.shape = shape
        self.kernel_size = kernel_size
        self.strides = strides
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: 4-D Tensor [batch, height, width, in_channels].

        Returns:
            4-D Tensor [batch, pooled height, pooled width, in_channels].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'
        strides = int_or_tuple(self.strides)
        filter_size = validate_filter_size(self.kernel_size, self.num_classes, input_shape[-1])

        if self.shape is None:
            # Compute shape out of Bottom
            in_shape = get_shape(incoming)

            h = ((in_shape[1] - 1) * strides[1]) + 1
            w = ((in_shape[2] - 1) * strides[1]) + 1
            new_shape = [in_shape[0], h, w, self.num_classes]
        else:
            new_shape = [self.shape[0], self.shape[1], self.shape[2], self.num_classes]
        output_shape = tf.stack(values=new_shape)

        def get_deconv_filter(f_shape):
            """Creates filter weights initialized as bi_linear upsampling."""
            width = f_shape[0]
            heigh = f_shape[0]
            f = ceil(width / 2.0)
            c = (2 * f - 1 - f % 2) / (2.0 * f)
            bi_linear = np.zeros([f_shape[0], f_shape[1]])
            for x in xrange(width):
                for y in xrange(heigh):
                    value = (1 - abs(x / f - c)) * (1 - abs(y / f - c))
                    bi_linear[x, y] = value
            weights = np.zeros(f_shape)
            for i in xrange(f_shape[2]):
                weights[:, :, i, i] = bi_linear

            init = tf.constant_initializer(value=weights, dtype=tf.float32)
            self._w = variable(name='up_filter', initializer=init, shape=weights.shape,
                               trainable=self.trainable, restore=self.restore)
            track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            return self._w

        weights = get_deconv_filter(filter_size)
        deconv = tf.nn.conv2d_transpose(value=incoming, filter=weights, output_shape=output_shape,
                                        strides=strides, padding='SAME')
        track(deconv, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return deconv


class Conv1d(BaseLayer):
    """Adds a Convolution 1D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: 'int` or `list of int`. Size of filters.
        strides: 'int` or `list of int`. Strides of conv operation.
            Default: [1 1 1 1].
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Conv1D'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        b: `Variable`. Variable representing biases.
    """
    def __init__(self, mode, num_filter, filter_size, strides=1, padding='SAME',
                 activation='linear', bias=True, weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name="Conv1D"):
        super(Conv1d, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 3-D Tensor [batch, steps, in_channels].

        Returns:
            3-D Tensor [batch, new steps, num_filters].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 3, 'Incoming Tensor shape must be 3-D'
        filter_size = validate_filter_size(self.filter_size, input_shape[-1], self.num_filter)
        filter_size[1] = 1
        strides = int_or_tuple(self.strides)
        strides = [1, strides[1], 1, 1]
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        self._w = variable('w', shape=filter_size, regularizer=regularizer,
                           initializer=getters.get_initializer(self.weights_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Adding dummy dimension to fit with Tensorflow conv2d
        inference = tf.expand_dims(input=incoming, axis=2)
        inference = tf.nn.conv2d(input=inference, filter=self._w, strides=strides, padding=padding)

        self._b = None
        if self.bias:
            self._b = variable('b', shape=self.num_filter,
                               initializer=getters.get_initializer(self.bias_init),
                               trainable=self.trainable, restore=self.restore)
            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            inference = tf.nn.bias_add(inference, self._b)

        inference = tf.squeeze(input=inference, axis=[2])

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Pool1dMixin(object):
    """A Mixin to add pooling 1d operation."""

    def _pool1d(self, incoming, fct):
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 3-D'

        kernel = int_or_tuple(self.kernel_size)
        kernel = [1, kernel[1], 1, 1]
        strides = int_or_tuple(self.strides) if self.strides else kernel
        strides = [1, strides[1], 1, 1]
        padding = validate_padding(self.padding)

        inference = tf.expand_dims(input=incoming, axis=2)
        inference = fct(inference, kernel, strides, padding)
        inference = tf.squeeze(input=inference, axis=[2])
        track(inference, tf.GraphKeys.ACTIVATIONS)
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class MaxPool1d(BaseLayer, Pool1dMixin):
    """Adds Max Pooling 1D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: `int` or `list of int`. Pooling kernel size.
        strides: `int` or `list of int`. Strides of conv operation.
            Default: SAME as kernel_size.
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        name: A name for this layer (optional). Default: 'MaxPool1D'.
    """
    def __init__(self, mode, kernel_size, strides=None, padding='SAME', name='MaxPool1D'):
        super(MaxPool1d, self).__init__(mode, name)
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 3-D Tensor [batch, steps, in_channels].

        Returns:
            3-D Tensor [batch, pooled steps, in_channels].
        """
        return self._pool1d(incoming, tf.nn.max_pool)


class AvgPool1d(BaseLayer, Pool1dMixin):
    """Average Pooling 1D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: `int` or `list of int`. Pooling kernel size.
        strides: `int` or `list of int`. Strides of conv operation.
            Default: SAME as kernel_size.
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        name: A name for this layer (optional). Default: 'AvgPool1D'.
    """
    def __init__(self, mode, kernel_size, strides=None, padding='SAME', name='AvgPool1D'):
        super(AvgPool1d, self).__init__(mode, name)
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 3-D Tensor [batch, steps, in_channels].

        Returns:
            3-D Tensor [batch, pooled steps, in_channels].
        """
        return self._pool1d(incoming, tf.nn.avg_pool)


class Conv3d(BaseLayer):
    """Adds Convolution 3D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: `int` or `list of int`. Size of filters.
        strides: 'int` or list of `int`. Strides of conv operation.
            Default: [1 1 1 1 1]. Must have strides[0] = strides[4] = 1.
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Conv3D'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        b: `Variable`. Variable representing biases.
    """
    def __init__(self, mode, num_filter, filter_size, strides=1, padding='SAME',
                 activation='linear', bias=True, weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name='Conv3D'):
        super(Conv3d, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 5-D Tensor [batch, in_depth, in_height, in_width, in_channels].

        Returns:
            5-D Tensor [filter_depth, filter_height, filter_width, in_channels, out_channels].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 5, 'Incoming Tensor shape must be 5-D'
        filter_size = validate_filter_size_3d(self.filter_size, input_shape[-1], self.num_filter)
        strides = int_or_tuple_3d(self.strides)
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        self._w = variable('w', shape=filter_size, regularizer=regularizer,
                           initializer=getters.get_initializer(self.weights_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        inference = tf.nn.conv3d(input=incoming, filter=self._w,
                                 strides=strides, padding=padding)

        self._b = None
        if self.bias:
            self._b = variable('b', shape=self.num_filter,
                               initializer=getters.get_initializer(self.bias_init),
                               trainable=self.trainable, restore=self.restore)
            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            inference = tf.nn.bias_add(value=inference, bias=self._b)

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)

        return inference


class Conv3dTranspose(BaseLayer):
    """Adds Convolution 3D Transpose.

    This operation is sometimes called "deconvolution" after (Deconvolutional
    Networks)[http://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf], but is
    actually the transpose (gradient) of `conv3d` rather than an actual
    deconvolution.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: `int` or `list of int`. Size of filters.
        output_shape: `list of int`. Dimensions of the output tensor.
            Can optionally include the number of conv filters.
            [new depth, new height, new width, num_filter]
            or [new depth, new height, new width].
        strides: `int` or list of `int`. Strides of conv operation.
            Default: [1 1 1 1 1].
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Conv2DTranspose'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        b: `Variable`. Variable representing biases.
    """
    def __init__(self, mode, num_filter, filter_size, output_shape, strides=1, padding='SAME',
                 activation='linear', bias=True, weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name='Conv3DTranspose'):
        super(Conv3dTranspose, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.output_shape = output_shape
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 5-D Tensor [batch, depth, height, width, in_channels].

        Returns:
            5-D Tensor [batch, new depth, new height, new width, num_filter].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 5, 'Incoming Tensor shape must be 5-D'

        filter_size = validate_filter_size_3d(self.filter_size, self.num_filter, input_shape[-1])
        strides = int_or_tuple_3d(self.strides)
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        self._w = variable('w', shape=filter_size, regularizer=regularizer,
                           initializer=getters.get_initializer(self.weights_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Determine the complete shape of the output tensor.
        batch_size = tf.gather(params=tf.shape(incoming), indices=tf.constant([0]))
        output_shape = self.output_shape
        if len(output_shape) == 3:
            output_shape = self.output_shape + [self.num_filter]
        elif len(output_shape) != 4:
            raise Exception('output_shape length error: {}, '
                            'only a length of 3 or 4 is supported.'.format(len(output_shape)))

        complete_out_shape = tf.concat(axis=0, values=[batch_size, tf.constant(output_shape)])

        inference = tf.nn.conv3d_transpose(
            value=incoming, filter=self._w, output_shape=complete_out_shape,
            strides=strides, padding=padding)
        # Reshape tensor so its shape is correct.
        inference.set_shape([None] + output_shape)

        self._b = None
        if self.bias:
            self._b = variable('b', shape=self.num_filter,
                               initializer=getters.get_initializer(self.bias_init),
                               trainable=self.trainable, restore=self.restore)
            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            inference = tf.nn.bias_add(value=inference, bias=self._b)

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Pool3dMixin(object):
    """Mixin to add pooling 3d operation."""

    def _pool3d(self, incoming, fct):
        input_shape = get_shape(incoming)
        assert len(input_shape) == 5, 'Incoming Tensor shape must be 5-D'

        kernel = int_or_tuple_3d(self.kernel_size)
        strides = int_or_tuple_3d(self.strides)
        padding = validate_padding(self.padding)

        inference = fct(incoming, kernel, strides, padding)
        track(inference, tf.GraphKeys.ACTIVATIONS)
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class MaxPool3d(BaseLayer, Pool3dMixin):
    """Max Pooling 3D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: 'int` or `list of int`. Pooling kernel size.
            Must have kernel_size[0] = kernel_size[1] = 1
        strides: 'int` or `list of int`. Strides of conv operation.
            Must have strides[0] = strides[4] = 1.
            Default: [1 1 1 1 1]
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        name: A name for this layer (optional). Default: 'MaxPool3D'.
    """
    def __init__(self, mode, kernel_size, strides=1, padding='SAME', name='MaxPool3D'):
        super(MaxPool3d, self).__init__(mode, name)
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 5-D Tensor [batch, depth, rows, cols, channels].

        Returns:
            5-D Tensor [batch, pooled depth, pooled rows, pooled cols, in_channels].
        """
        return self._pool3d(incoming, tf.nn.max_pool3d)


class AvgPool3d(BaseLayer, Pool3dMixin):
    """Average Pooling 3D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        kernel_size: 'int` or `list of int`. Pooling kernel size.
            Must have kernel_size[0] = kernel_size[1] = 1
        strides: 'int` or `list of int`. Strides of conv operation.
            Must have strides[0] = strides[4] = 1.
            Default: [1 1 1 1 1]
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        name: A name for this layer (optional). Default: 'AvgPool3D'.
    """
    def __init__(self, mode, kernel_size, strides=None, padding='SAME', name='AvgPool3D'):
        super(AvgPool3d, self).__init__(mode, name)
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 5-D Tensor [batch, depth, rows, cols, channels].

        Returns:
            5-D Tensor [batch, pooled depth, pooled rows, pooled cols, in_channels].
        """
        return self._pool3d(incoming, tf.nn.avg_pool3d)


class GlobalPoolMixin(object):
    """A Mixin to add global pool operation."""

    def _global_pool(self, incoming, fct):
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'

        inference = fct(incoming, [1, 2])
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class GlobalMaxPool(BaseLayer, GlobalPoolMixin):
    """Adds a Global Max Pooling.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: A name for this layer (optional). Default: 'GlobalMaxPool'.
    """
    def __init__(self, mode, name='GlobalMaxPool'):
        super(GlobalMaxPool, self).__init__(mode, name)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 4-D Tensor [batch, height, width, in_channels].

        Returns:
            2-D Tensor [batch, pooled dim]
        """
        return self._global_pool(incoming, tf.reduce_max)


class GlobalAvgPool(BaseLayer, GlobalPoolMixin):
    """Adds a Global Average Pooling.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: A name for this layer (optional). Default: 'GlobalAvgPool'.
    """
    def __init__(self, mode, name='GlobalAvgPool'):
        super(GlobalAvgPool, self).__init__(mode, name)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 4-D Tensor [batch, height, width, in_channels].

        Returns:
            2-D Tensor [batch, pooled dim]
        """
        return self._gloabel_pool(incoming, tf.reduce_mean)


class ResidualBlock(BaseLayer):
    """Adds a Residual Block.

    A residual block as described in MSRA's Deep Residual Network paper.
    Full pre-activation architecture is used here.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        nb_blocks: `int`. Number of layer blocks.
        out_channels: `int`. The number of convolutional filters of the
            convolution layers.
        downsample: `bool`. If True, apply downsampling using
            'downsample_strides' for strides.
        downsample_strides: `int`. The strides to use when downsampling.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        batch_norm: `bool`. If True, apply batch normalization.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'uniform_scaling'.
        bias_init: `str` (name) or `tf.Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'ShallowBottleneck'.

    References:
        - Deep Residual Learning for Image Recognition. Kaiming He, Xiangyu
            Zhang, Shaoqing Ren, Jian Sun. 2015.
        - Identity Mappings in Deep Residual Networks. Kaiming He, Xiangyu
            Zhang, Shaoqing Ren, Jian Sun. 2015.

    Links:
        - [http://arxiv.org/pdf/1512.03385v1.pdf]
            (http://arxiv.org/pdf/1512.03385v1.pdf)
        - [Identity Mappings in Deep Residual Networks]
            (https://arxiv.org/pdf/1603.05027v2.pdf)
    """
    def __init__(self, mode, nb_blocks, out_channels, downsample=False, downsample_strides=2,
                 activation='relu', batch_norm=True, bias=True, weights_init='variance_scaling',
                 bias_init='zeros', regularizer='L2', scale=0.0001,
                 trainable=True, restore=True, name='ResidualBlock'):
        super(ResidualBlock, self).__init__(mode, name)
        self.nb_blocks = nb_blocks
        self.out_channels = out_channels
        self.downsample = downsample
        self.downsample_strides = downsample_strides if self.downsample else 1
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore
        self.batch_norm = batch_norm

    def _declare_dependencies(self):
        self._conv2d_1 = Conv2d(self.mode, self.out_channels, 3, self.downsample_strides,
                                'SAME', 'linear', self.bias, self.weights_init, self.bias_init,
                                self.regularizer, self.scale, self.trainable, self.restore)
        self._conv2d_2 = Conv2d(self.mode, self.out_channels, 3, 1, 'SAME', 'linear',
                                self.bias, self.weights_init, self.bias_init, self.regularizer,
                                self.scale, self.trainable, self.restore)
        if self.downsample_strides > 1:
            self._avg_pool2d = AvgPool2d(
                self.mode, self.downsample_strides, self.downsample_strides)
        else:
            self._avg_pool2d = None

        self._batch_norm1 = None
        self._batch_norm2 = None
        if self.batch_norm:
            self._batch_norm1 = BatchNormalization(self.mode)
            self._batch_norm2 = BatchNormalization(self.mode)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 4-D Tensor [batch, height, width, in_channels].

        Returns:
            4-D Tensor [batch, new height, new width, num_filter].
        """
        self._declare_dependencies()
        resnet = incoming
        in_channels = get_shape(incoming)[-1]

        for i in xrange(self.nb_blocks):
            identity = resnet

            if self._batch_norm1:
                resnet = self._batch_norm1(resnet)
            resnet = getters.get_activation(self.activation)(resnet)

            resnet = self._conv2d_1(resnet)

            if self.batch_norm:
                resnet = self._batch_norm2(resnet)
            resnet = getters.get_activation(self.activation)(resnet)

            resnet = self._conv2d_2(resnet)

            # Downsampling
            if self.downsample_strides > 1:
                identity = self._avg_pool2d(identity)

            # Projection to new dimension
            if in_channels != self.out_channels:
                ch = (self.out_channels - in_channels) // 2
                identity = tf.pad(tensor=identity, paddings=[[0, 0], [0, 0], [0, 0], [ch, ch]])
                in_channels = self.out_channels

            resnet = resnet + identity

        return resnet


class ResidualBottleneck(BaseLayer):
    """Adds a Residual Bottleneck.

    A residual bottleneck block as described in MSRA's Deep Residual Network
    paper. Full pre-activation architecture is used here.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        nb_blocks: `int`. Number of layer blocks.
        bottleneck_size: `int`. The number of convolutional filter of the
            bottleneck convolutional layer.
        out_channels: `int`. The number of convolutional filters of the
            layers surrounding the bottleneck layer.
        downsample: `bool`. If True, apply downsampling using
            'downsample_strides' for strides.
        downsample_strides: `int`. The strides to use when downsampling.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        batch_norm: `bool`. If True, apply batch normalization.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'uniform_scaling'.
        bias_init: `str` (name) or `tf.Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'DeepBottleneck'.

    References:
        - Deep Residual Learning for Image Recognition. Kaiming He, Xiangyu
            Zhang, Shaoqing Ren, Jian Sun. 2015.
        - Identity Mappings in Deep Residual Networks. Kaiming He, Xiangyu
            Zhang, Shaoqing Ren, Jian Sun. 2015.

    Links:
        - [http://arxiv.org/pdf/1512.03385v1.pdf]
            (http://arxiv.org/pdf/1512.03385v1.pdf)
        - [Identity Mappings in Deep Residual Networks]
            (https://arxiv.org/pdf/1603.05027v2.pdf)
    """
    def __init__(self, mode, nb_blocks, bottleneck_size, out_channels, downsample=False,
                 downsample_strides=2, activation='relu', batch_norm=True, bias=True,
                 weights_init='variance_scaling', bias_init='zeros', regularizer='L2',
                 scale=0.0001, trainable=True, restore=True, name="ResidualBottleneck"):
        super(ResidualBottleneck, self).__init__(mode, name)
        self.nb_blocks = nb_blocks
        self.bottleneck_size = bottleneck_size
        self.out_channels = out_channels
        self.downsample = downsample
        self.downsample_strides = downsample_strides if self.downsample else 1
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore
        self.batch_norm = batch_norm

    def _declare_dependencies(self):
        self._conv2d_1 = Conv2d(
            self.mode, self.bottleneck_size, 1, self.downsample_strides, 'VALID', 'linear',
            self.bias, self.weights_init, self.bias_init, self.regularizer, self.scale,
            self.trainable, self.restore)
        self._conv2d_2 = Conv2d(
            self.mode, self.bottleneck_size, 3, 1, 'SAME', 'linear', self.bias, self.weights_init,
            self.bias_init, self.regularizer, self.scale, self.trainable, self.restore)
        self._conv2d_3 = Conv2d(
            self.mode, self.out_channels, 1, 1, 'VALID', self.activation, self.bias,
            self.weights_init, self.bias_init, self.regularizer, self.scale, self.trainable,
            self.restore)
        if self.downsample_strides > 1:
            self._avg_pool2d = AvgPool2d(
                self.mode, self.downsample_strides, self.downsample_strides)
        else:
            self._avg_pool2d = None

        self._batch_norm1 = None
        self._batch_norm2 = None
        if self.batch_norm:
            self._batch_norm1 = BatchNormalization(self.mode)
            self._batch_norm2 = BatchNormalization(self.mode)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 4-D Tensor [batch, height, width, in_channels].

        Returns:
            4-D Tensor [batch, new height, new width, num_filter].
        """
        self._declare_dependencies()

        resnet = incoming
        in_channels = get_shape(incoming)[-1]

        for i in xrange(self.nb_blocks):
            identity = resnet

            if self._batch_norm1:
                resnet = self._batch_norm1(resnet)
            resnet = getters.get_activation(self.activation)(resnet)

            resnet = self._conv2d_1(resnet)

            if self._batch_norm2:
                resnet = self._batch_norm2(resnet)
            resnet = getters.get_activation(self.activation)(resnet)

            resnet = self._conv2d_2(resnet)
            resnet = self._conv2d_3(resnet)

            # Downsampling
            if self.downsample_strides > 1:
                identity = self._avg_pool2d(identity)

            # Projection to new dimension
            if in_channels != self.out_channels:
                ch = (self.out_channels - in_channels) // 2
                identity = tf.pad(tensor=identity, paddings=[[0, 0], [0, 0], [0, 0], [ch, ch]])
                in_channels = self.out_channels

                resnet = resnet + identity
                resnet = getters.get_activation(self.activation)(resnet)

        return resnet


class HighwayConv2d(BaseLayer):
    """Adds a Highway Convolution 2D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: 'int` or `list of int`. Size of filters.
        strides: 'int` or `list of int`. Strides of conv operation.
            Default: [1 1 1 1].
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Conv2D'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        w_t: `Variable`. Variable representing gate weights.
        b: `Variable`. Variable representing biases.
        b_t: `Variable`. Variable representing gate biases.
    """
    def __init__(self, mode, num_filter, filter_size, strides=1, padding='SAME',
                 activation='linear', weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name="HighwayConv2D"):
        super(HighwayConv2d, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

        self.name = name

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    @property
    def w_t(self):
        return self._w_t

    @property
    def b_t(self):
        return self._b_t

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 4-D Tensor [batch, height, width, in_channels].
        Returns:
            4-D Tensor [batch, new height, new width, num_filter].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 4, 'Incoming Tensor shape must be 4-D'
        filter_size = validate_filter_size(
            self.filter_size, input_shape[-1], self.num_filter)
        strides = int_or_tuple(self.strides)
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        w_initializer = getters.get_initializer(self.weights_init)
        self._w = variable('w', shape=filter_size, regularizer=regularizer,
                           initializer=w_initializer, trainable=self.trainable,
                           restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        self._b = variable('b', shape=self.num_filter,
                           initializer=getters.get_initializer(self.bias_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Weight and bias for the transform gate
        self._w_t = variable(
            'w_t', shape=self.num_filter, regularizer=None, initializer=w_initializer,
            trainable=self.trainable, restore=self.restore)
        track(self._w_t, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        self._b_t = variable(
            'b_T', shape=self.num_filter, initializer=tf.constant_initializer(-3),
            trainable=self.trainable, restore=self.restore)
        track(self._b_t, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Shared convolution for gating
        convolved = tf.nn.conv2d(input=incoming, filter=self._w,
                                 strides=strides, padding=padding)
        H = getters.get_activation(self.activation)(convolved + self._b)
        T = tf.sigmoid(x=tf.multiply(convolved, self._w_t) + self._b_t)
        C = tf.subtract(x=1.0, y=T)
        inference = tf.add(x=tf.multiply(x=H, y=T), y=tf.multiply(x=convolved, y=C))
        track(inference, tf.GraphKeys.ACTIVATIONS)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class HighwayConv1d(BaseLayer):
    """Adds a Highway Convolution 1D.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_filter: `int`. The number of convolutional filters.
        filter_size: 'int` or `list of int`. Size of filters.
        strides: 'int` or `list of int`. Strides of conv operation.
            Default: [1 1 1 1].
        padding: `str` from `"SAME", "VALID"`. Padding algo to use.
            Default: 'SAME'.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        bias_init: `str` (name) or `Tensor`. Bias initialization.
            Default: 'zeros'.
        regularizer: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
            Default: None.
        scale: `float`. Regularizer decay parameter. Default: 0.001.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'HighwayConv1D'.

    Attributes:
        w: `Variable`. Variable representing filter weights.
        w_t: `Variable`. Variable representing gate weights.
        b: `Variable`. Variable representing biases.
        b_t: `Variable`. Variable representing gate biases.
    """
    def __init__(self, mode, num_filter, filter_size, strides=1, padding='SAME',
                 activation='linear', weights_init='uniform_scaling',
                 bias_init='zeros', regularizer=None, scale=0.001,
                 trainable=True, restore=True, name="HighwayConv1D"):
        super(HighwayConv1d, self).__init__(mode, name)
        self.num_filter = num_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.activation = activation
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    @property
    def w_t(self):
        return self._w_t

    @property
    def b_t(self):
        return self._b_t

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 3-D Tensor [batch, steps, in_channels].
        Returns:
            3-D Tensor [batch, new steps, num_filters].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 3, 'Incoming Tensor shape must be 3-D'
        filter_size = validate_filter_size(self.filter_size, input_shape[-1], self.num_filter)
        filter_size[1] = 1
        strides = int_or_tuple(self.strides)
        strides[1] = 1
        padding = validate_padding(self.padding)
        incoming = validate_dtype(incoming)

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        w_initializer = getters.get_initializer(self.weights_init)
        self._w = variable(
            'w', shape=filter_size, regularizer=regularizer, initializer=w_initializer,
            trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        self._b = variable(
            'b', shape=self.num_filter, initializer=getters.get_initializer(self.bias_init),
            trainable=self.trainable, restore=self.restore)
        track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Weight and bias for the transform gate
        self._w_t = variable(
            'w_t', shape=self.num_filter, regularizer=None, initializer=w_initializer,
            trainable=self.trainable, restore=self.restore)
        track(self._w_t, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        self._b_t = variable(
            'b_T', shape=self.num_filter, initializer=tf.constant_initializer(-3),
            trainable=self.trainable, restore=self.restore)
        track(self._b_t, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Adding dummy dimension to fit with Tensorflow conv2d
        inference = tf.expand_dims(input=incoming, axis=2)
        # Shared convolution for gating
        convolved = tf.nn.conv2d(
            input=inference, filter=self._w, strides=strides, padding=padding)
        H = getters.get_activation(self.activation)(tf.squeeze(convolved + self._b, [2]))
        T = tf.sigmoid(
            x=tf.squeeze(input=tf.multiply(convolved, self._w_t) + self._b_t, axis=[2]))
        C = tf.subtract(x=1.0, y=T)
        Q = tf.multiply(x=H, y=T)
        R = tf.multiply(x=tf.squeeze(input=convolved, axis=[2]), y=C)
        inference = tf.add(x=Q, y=R)
        track(inference, tf.GraphKeys.ACTIVATIONS)

        # Add attributes to Tensor to easy access weights.
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference
