# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from six.moves import xrange

import numpy as np
import tensorflow as tf

from tensorflow.python.framework import dtypes
from tensorflow.python.ops import standard_ops

from polyaxon import ModeKeys
from polyaxon.libs import getters
from polyaxon.libs.template_module import BaseLayer
from polyaxon.libs.utils import get_shape, track, validate_dtype
from polyaxon.variables import variable


class FullyConnected(BaseLayer):
    """Adds a fully connected layer.

    `fully_connected` creates a variable called `w`, representing a fully
    connected weight matrix, which is multiplied by the `incoming` to produce a
    `Tensor` of hidden units.

    Note: that if `inputs` have a rank greater than 2, then `inputs` is flattened
    prior to the initial matrix multiply by `weights`.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        n_units: `int`, number of units for this layer.
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
        dropout: `float`. Adds a dropout with `keep_prob` as `1 - dropout`.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'FullyConnected'.

    Attributes:
        w: `Tensor`. Variable representing units weights.
        b: `Tensor`. Variable representing biases.
    """
    def __init__(self, mode, n_units, activation='linear', bias=True,
                 weights_init='truncated_normal', bias_init='zeros', regularizer=None,
                 scale=0.001, dropout=None, trainable=True, restore=True, name="FullyConnected"):
        super(FullyConnected, self).__init__(mode, name)
        self.n_units = n_units
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.dropout = dropout
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _declare_dependencies(self):
        self._dropout = None
        if self.dropout:
            self._dropout = Dropout(mode=self.mode, keep_prob=(1 - self.dropout))

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: (2+)-D Tensor [samples, input dim]. If not 2D, input will be flatten.

        Returns:
            2D Tensor [samples, n_units].
        """
        self._declare_dependencies()
        input_shape = get_shape(incoming)
        incoming = validate_dtype(incoming)

        assert len(input_shape) > 1, 'Incoming Tensor shape must be at least 2-D'
        n_inputs = int(np.prod(input_shape[1:]))

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        self._w = variable(
            name='w', shape=[n_inputs, self.n_units], dtype=incoming.dtype, regularizer=regularizer,
            initializer=getters.get_initializer(self.weights_init), trainable=self.trainable,
            restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        inference = incoming
        # If input is not 2d, flatten it.
        if len(input_shape) > 2:
            inference = tf.reshape(tensor=inference, shape=[-1, n_inputs])
        inference = tf.matmul(a=inference, b=self._w)

        self._b = None
        if self.bias:
            self._b = variable(name='b', shape=[self.n_units], dtype=incoming.dtype,
                               initializer=getters.get_initializer(self.bias_init),
                               trainable=self.trainable, restore=self.restore)
            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            inference = tf.nn.bias_add(value=inference, bias=self._b)

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        if self._dropout:
            inference = self._dropout(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Dropout(BaseLayer):
    """Adds a Dropout op to the input.

    Outputs the input element scaled up by `1 / keep_prob`. The scaling is so
    that the expected sum is unchanged.

    By default, each element is kept or dropped independently. If noise_shape
    is specified, it must be broadcastable to the shape of x, and only dimensions
    with noise_shape[i] == shape(x)[i] will make independent decisions. For
    example, if shape(x) = [k, l, m, n] and noise_shape = [k, 1, 1, n], each
    batch and channel component will be kept independently and each row and column
    will be kept or not kept together.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        keep_prob : A float representing the probability that each element
            is kept.
        noise_shape : A 1-D Tensor of type int32, representing the shape for
            randomly generated keep/drop flags.
        name : A name for this layer (optional).

    References:
        Dropout: A Simple Way to Prevent Neural Networks from Overfitting.
        N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever & R. Salakhutdinov,
        (2014), Journal of Machine Learning Research, 5(Jun)(2), 1929-1958.

    Links:
      [https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf]
        (https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf)
    """
    def __init__(self, mode, keep_prob, noise_shape=None, seed=None, name='Dropout'):
        super(Dropout, self).__init__(mode, name)
        self.keep_prob = keep_prob
        self.noise_shape = noise_shape
        self.seed = seed

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming : A `Tensor`. The incoming tensor.
        """
        inference = incoming

        def apply_dropout():
            if isinstance(self.keep_prob, float):
                _keep_prob = tf.get_variable(
                    name='keep_prob', shape=[],
                    initializer=tf.constant_initializer(self.keep_prob), trainable=False)
            tf.add_to_collection(tf.GraphKeys.DROPOUTS, _keep_prob)
            if type(inference) in [list, np.array]:
                for x in inference:
                    tf.nn.dropout(x=x, keep_prob=_keep_prob,
                                  noise_shape=self.noise_shape, seed=self.seed)
                return inference
            else:
                return tf.nn.dropout(x=inference, keep_prob=_keep_prob,
                                     noise_shape=self.noise_shape, seed=self.seed)

        if self.mode == ModeKeys.TRAIN:
            inference = apply_dropout()
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Reshape(BaseLayer):
    """Reshape.

    A layer that reshape the incoming layer tensor output to the desired shape.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        new_shape: A list of `int`. The desired shape.
        name: A name for this layer (optional).
    """
    def __init__(self, mode, new_shape, name='Reshape'):
        super(Reshape, self).__init__(mode, name)
        self.new_shape = new_shape

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: A `Tensor`. The incoming tensor.
        """
        inference = incoming
        if isinstance(inference, list):
            inference = tf.concat(axis=inference, values=0)
            inference = tf.cast(x=inference, dtype=tf.float32)
        inference = tf.reshape(tensor=inference, shape=self.new_shape)
        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Flatten(BaseLayer):
    """Flatten the incoming Tensor.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: A name for this layer (optional).
    """
    def __init__(self, mode, name='Flatten'):
        super(Flatten, self).__init__(mode, name)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: (2+)-D `Tensor`.

        Returns:
            2-D `Tensor` [batch, flatten_dims].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) > 1, 'Incoming Tensor shape must be at least 2-D'
        dims = int(np.prod(input_shape[1:]))
        x = tf.reshape(tensor=incoming, shape=[-1, dims])
        track(x, tf.GraphKeys.LAYER_TENSOR, self.name)
        return x


class SingleUnit(BaseLayer):
    """Adds a Single Unit Layer.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        activation: `str` (name) or `function`. Activation applied to this layer. Default: 'linear'.
        bias: `bool`. If True, a bias is used.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Linear'.

    Attributes:
        W: `Tensor`. Variable representing weight.
        b: `Tensor`. Variable representing bias.
    """
    def __init__(self, mode, activation='linear', bias=True, trainable=True, restore=True,
                 name='Linear'):
        super(SingleUnit, self).__init__(mode, name)
        self.activation = activation
        self.bias = bias
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
            incoming: 1-D Tensor [samples]. If not 2D, input will be flatten.

        Returns:
            1-D Tensor [samples].
        """
        input_shape = get_shape(incoming)
        n_inputs = int(np.prod(a=input_shape[1:]))

        initializer = tf.constant_initializer(value=np.random.randn())
        self._w = variable(name='w', shape=[n_inputs],
                           dtype=incoming.dtype, initializer=initializer,
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        inference = incoming
        # If input is not 2d, flatten it.
        if len(input_shape) > 1:
            inference = tf.reshape(tensor=inference, shape=[-1])
        inference = tf.multiply(x=inference, y=self._w)

        self._b = None
        if self.bias:
            self._b = variable(name='b', shape=[n_inputs],
                               dtype=incoming.dtype, initializer=initializer,
                               trainable=self.trainable, restore=self.restore)
            inference = tf.add(inference, self._b)
            track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        if self.activation:
            inference = getters.get_activation(self.activation, collect=True)(inference)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class Highway(BaseLayer):
    """Adds Fully Connected Highway.

    A fully connected highway network layer, with some inspiration from
    [https://github.com/fomorians/highway-fcn](https://github.com/fomorians/highway-fcn).

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        n_units: `int`, number of units for this layer.
        activation: `str` (name) or `function` (returning a `Tensor`).
            Default: 'linear'.
        transform_dropout: `float`: Keep probability on the highway transform gate.
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
        name: A name for this layer (optional). Default: 'FullyConnectedHighway'.

    Attributes:
        W: `Tensor`. Variable representing units weights.
        W_t: `Tensor`. Variable representing units weights for transform gate.
        b: `Tensor`. Variable representing biases.
        b_t: `Tensor`. Variable representing biases for transform gate.

    Links:
        [https://arxiv.org/abs/1505.00387](https://arxiv.org/abs/1505.00387)
    """
    def __init__(self, mode, n_units, activation='linear', transform_dropout=None,
                 weights_init='truncated_normal', bias_init='zeros',
                 regularizer=None, scale=0.001, trainable=True,
                 restore=True, name='FullyConnectedHighway'):
        super(Highway, self).__init__(mode, name)
        self.n_units = n_units
        self.activation = activation
        self.weights_init = weights_init
        self.bias_init = bias_init
        self.regularizer = regularizer
        self.scale = scale
        self.trainable = trainable
        self.restore = restore

        self.transform_dropout = transform_dropout

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

    def _declare_dependencies(self):
        self._transform_dropout = None
        if self.transform_dropout:
            self._transform_dropout = Dropout(self.mode, keep_prob=1 - self.transform_dropout)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: (2+)-D Tensor [samples, input dim]. If not 2D, input will be flatten.

        Returns:
            2D Tensor [samples, n_units].
        """
        self._declare_dependencies()
        input_shape = get_shape(incoming)
        assert len(input_shape) > 1, 'Incoming Tensor shape must be at least 2-D'
        n_inputs = int(np.prod(input_shape[1:]))

        regularizer = getters.get_regularizer(self.regularizer, scale=self.scale, collect=True)
        initializer = getters.get_initializer(self.weights_init)
        self._w = variable(name='w', shape=[n_inputs, self.n_units], regularizer=regularizer,
                           initializer=initializer, trainable=self.trainable,
                           restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        self._b = variable(name='b', shape=[self.n_units],
                           initializer=getters.get_initializer(self.bias_init),
                           trainable=self.trainable, restore=self.restore)
        track(self._b, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # Weight and bias for the transform gate
        self._w_t = variable(name='w_t', shape=[n_inputs, self.n_units],
                             regularizer=None, initializer=initializer,
                             trainable=self.trainable, restore=self.restore)
        track(self._w_t, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        self._b_t = variable(name='b_t', shape=[self.n_units],
                             initializer=tf.constant_initializer(-1),
                             trainable=self.trainable, restore=self.restore)
        track(self._b_t, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        # If input is not 2d, flatten it.
        if len(input_shape) > 2:
            incoming = tf.reshape(tensor=incoming, shape=[-1, n_inputs])

        H = getters.get_activation(self.activation)(tf.matmul(a=incoming, b=self._w) + self._b)
        T = tf.sigmoid(tf.matmul(a=incoming, b=self._w_t) + self._b_t)
        if self._transform_dropout:
            T = self._transform_dropout(T)
        C = tf.subtract(x=1.0, y=T)
        inference = tf.add(x=tf.multiply(x=H, y=T), y=tf.multiply(x=incoming, y=C))
        track(inference, tf.GraphKeys.ACTIVATIONS)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


class OneHotEncoding(BaseLayer):
    """Transform numeric labels into one hot labels using `tf.one_hot`.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        n_classes: `int`. Total number of classes.
        on_value: `scalar`. A scalar defining the on-value.
        off_value: `scalar`. A scalar defining the off-value.
        name: A name for this layer (optional). Default: 'OneHotEncoding'.
    """
    def __init__(self, mode, n_classes, on_value=1.0, off_value=0.0, name='OneHotEncoding'):
        super(OneHotEncoding, self).__init__(mode, name)
        self.n_classes = n_classes
        self.on_value = on_value
        self.off_value = off_value

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: The Labels Placeholder.
        Returns:
            2-D Tensor, The encoded labels.
        """
        if incoming.dtype != dtypes.int64:
            incoming = standard_ops.to_int64(incoming)

        incoming = standard_ops.one_hot(indices=incoming, depth=self.n_classes,
                                        on_value=self.on_value, off_value=self.off_value)
        track(incoming, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return incoming


class Merge(BaseLayer):
    class MergeMode(object):
        CONCAT = 'concat'
        ELEMENTWISE_SUM = 'elemwise_sum'
        ELEMENTWISE_MUL = 'elemwise_mul'
        SUM = 'sum'
        MEAN = 'mean'
        PROD = 'prod'
        MAX = 'max'
        MIN = 'min'
        AND = 'and'
        OR = 'or'

        MODES = [CONCAT, ELEMENTWISE_SUM, ELEMENTWISE_MUL, ELEMENTWISE_MUL,
                 SUM, MEAN, PROD, MAX, MIN, AND, OR]

    def __init__(self, mode, merge_mode, axis=1, name='Merge'):
        """Adds a merge op.

        Merge a list of `Tensor` into a single one. A merging 'mode' must be
        specified, check below for the different options.

        Args:
            mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
            merge_mode: `str`. Merging mode, value in `MERGE_MODE`
            axis: `int`. Represents the axis to use for merging mode.
                In most cases: 0 for concat and 1 for other modes.
            name: A name for this layer (optional).
        """
        super(Merge, self).__init__(mode, name)
        assert merge_mode in self.MergeMode.MODES, 'Merge mode `{}` not supported.'.format(merge_mode)
        self.merge_mode = merge_mode
        self.axis = axis

    def _build(self, dependencies, *args, **kwargs):
        """
        Args:
            incoming: List of Tensors.
        Returns:
            Merged Tensors.
        """
        assert len(dependencies) > 1, 'Merge required 2 or more tensors.'

        if self.merge_mode == self.MergeMode.CONCAT:
            x = tf.concat(axis=self.axis, values=dependencies)
        elif self.merge_mode == self.MergeMode.ELEMENTWISE_SUM:
            x = dependencies[0]
            for i in xrange(1, len(dependencies)):
                x = tf.add(x, dependencies[i])
        elif self.merge_mode == self.MergeMode.ELEMENTWISE_MUL:
            x = dependencies[0]
            for i in xrange(1, len(dependencies)):
                x = tf.multiply(x, dependencies[i])
        elif self.merge_mode == self.MergeMode.SUM:
            x = tf.reduce_sum(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        elif self.merge_mode == self.MergeMode.MEAN:
            x = tf.reduce_mean(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        elif self.merge_mode == self.MergeMode.PROD:
            x = tf.reduce_prod(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        elif self.merge_mode == self.MergeMode.MAX:
            x = tf.reduce_max(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        elif self.merge_mode == self.MergeMode.MIN:
            x = tf.reduce_min(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        elif self.merge_mode == self.MergeMode.AND:
            x = tf.reduce_all(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        elif self.merge_mode == self.MergeMode.OR:
            x = tf.reduce_any(tf.concat(axis=self.axis, values=dependencies), axis=self.axis)
        else:
            raise Exception('Unknown merge mode', str(self.merge_mode))

        track(x, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return x


class Concat(BaseLayer):
    """Concat Outputs.

    A layer that concatenate all outputs of a network into a single tensor.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. A name for this layer (optional).
    """
    def __init__(self, mode, name='Concat'):
        super(Concat, self).__init__(mode, name)

    def _build(self, dependencies, *args, **kwargs):
        """
        Args:
            dependencies: List of Tensors [_shape_].
        Returns:
            Concatenated Tensors [nb_tensors, _shape_].
        """
        x = tf.concat(axis=1, values=dependencies)
        track(x, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return x


class Slice(BaseLayer):
    """Extracts a slice from a tensor.

    This operation extracts a slice of size size from a tensor input starting at
    the location specified by begin.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. A name for this layer (optional).
    """
    def __init__(self, mode, begin, size, name='Slice'):
        super(Slice, self).__init__(mode, name)
        self.being = begin
        self.size = size

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: List of Tensors [_shape_].
        Returns:
            Concatenated Tensors [nb_tensors, _shape_].
        """
        x = tf.slice(incoming, begin=self.being, size=self.size)
        track(x, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return x
