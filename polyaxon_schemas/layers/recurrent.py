# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_dump, post_load, validate

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import (
    GlorotUniformInitializerConfig,
    InitializerSchema,
    OrthogonalInitializerConfig,
    ZerosInitializerConfig
)
from polyaxon_schemas.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.utils import ACTIVATION_VALUES, StrOrFct


class RecurrentSchema(BaseLayerSchema):
    return_sequences = fields.Bool(default=False, missing=False)
    return_state = fields.Bool(default=False, missing=False)
    go_backwards = fields.Bool(default=False, missing=False)
    stateful = fields.Bool(default=False, missing=False)
    unroll = fields.Bool(default=False, missing=False)
    implementation = fields.Int(default=0, missing=0)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RecurrentConfig(**data)

    @post_dump
    def unmake(self, data):
        return RecurrentConfig.remove_reduced_attrs(data)


class RecurrentConfig(BaseLayerConfig):
    """Abstract base class for recurrent layers.

    Do not use in a model -- it's not a valid layer!
    Use its children classes `LSTM`, `GRU` and `SimpleRNN` instead.

    All recurrent layers (`LSTM`, `GRU`, `SimpleRNN`) also
    follow the specifications of this class and accept
    the keyword arguments listed below.

    Example:

    ```python
        # as the first layer in a Sequential model
        model = Sequential()
        model.add(LSTM(32, input_shape=(10, 64)))
        # now model.output_shape == (None, 32)
        # note: `None` is the batch dimension.

        # for subsequent layers, no need to specify the input size:
        model.add(LSTM(16))

        # to stack recurrent layers, you must use return_sequences=True
        # on any recurrent layer that feeds into another recurrent layer.
        # note that you only need to specify the input size on the first layer.
        model = Sequential()
        model.add(LSTM(64, input_dim=64, input_length=10, return_sequences=True))
        model.add(LSTM(32, return_sequences=True))
        model.add(LSTM(10))
    ```

    Args:
        weights: list of Numpy arrays to set as initial weights.
            The list should have 3 elements, of shapes:
            `[(input_dim, output_dim), (output_dim, output_dim), (output_dim,)]`.
        return_sequences: Boolean. Whether to return the last output
            in the output sequence, or the full sequence.
        return_state: Boolean. Whether to return the last state
            in addition to the output.
        go_backwards: Boolean (default False).
            If True, process the input sequence backwards and return the
            reversed sequence.
        stateful: Boolean (default False). If True, the last state
            for each sample at index i in a batch will be used as initial
            state for the sample of index i in the following batch.
        unroll: Boolean (default False).
            If True, the network will be unrolled,
            else a symbolic loop will be used.
            Unrolling can speed-up a RNN,
            although it tends to be more memory-intensive.
            Unrolling is only suitable for short sequences.
        implementation: one of {0, 1, or 2}.
            If set to 0, the RNN will use
            an implementation that uses fewer, larger matrix products,
            thus running faster on CPU but consuming more memory.
            If set to 1, the RNN will use more matrix products,
            but smaller ones, thus running slower
            (may actually be faster on GPU) while consuming less memory.
            If set to 2 (LSTM/GRU only),
            the RNN will combine the input gate,
            the forget gate and the output gate into a single matrix,
            enabling more time-efficient parallelization on the GPU.
            Note: RNN dropout must be shared for all gates,
            resulting in a slightly reduced regularization.
        input_dim: dimensionality of the input (integer).
            This argument (or alternatively, the keyword argument `input_shape`)
            is required when using this layer as the first layer in a model.
        input_length: Length of input sequences, to be specified
            when it is constant.
            This argument is required if you are going to connect
            `Flatten` then `Dense` layers upstream
            (without it, the shape of the dense outputs cannot be computed).
            Note that if the recurrent layer is not the first layer
            in your model, you would need to specify the input length
            at the level of the first layer
            (e.g. via the `input_shape` argument)

    Input shape:s
        3D tensor with shape `(batch_size, timesteps, input_dim)`,
        (Optional) 2D tensors with shape `(batch_size, output_dim)`.

    Output shape:
        - if `return_state`: a list of tensors. The first tensor is
            the output. The remaining tensors are the last states,
            each with shape `(batch_size, units)`.
        - if `return_sequences`: 3D tensor with shape
            `(batch_size, timesteps, units)`.
        - else, 2D tensor with shape `(batch_size, units)`.

    # Masking
        This layer supports masking for input data with a variable number
        of timesteps. To introduce masks to your data,
        use an `Embedding` layer with the `mask_zero` parameter
        set to `True`.

    # Note on using statefulness in RNNs
        You can set RNN layers to be 'stateful', which means that the states
        computed for the samples in one batch will be reused as initial states
        for the samples in the next batch. This assumes a one-to-one mapping
        between samples in different successive batches.

        To enable statefulness:
            - specify `stateful=True` in the layer constructor.
            - specify a fixed batch size for your model, by passing
                if sequential model:
                  `batch_input_shape=(...)` to the first layer in your model.
                else for functional model with 1 or more Input layers:
                  `batch_shape=(...)` to all the first layers in your model.
                This is the expected shape of your inputs
                *including the batch size*.
                It should be a tuple of integers, e.g. `(32, 10, 100)`.
            - specify `shuffle=False` when calling fit().

        To reset the states of your model, call `.reset_states()` on either
        a specific layer, or on your entire model.

    # Note on specifying the initial state of RNNs
        You can specify the initial state of RNN layers symbolically by
        calling them with the keyword argument `initial_state`. The value of
        `initial_state` should be a tensor or list of tensors representing
        the initial state of the RNN layer.

        You can specify the initial state of RNN layers numerically by
        calling `reset_states` with the keyword argument `states`. The value of
        `states` should be a numpy array or list of numpy arrays representing
        the initial state of the RNN layer.
    """
    IDENTIFIER = 'Recurrent'
    SCHEMA = RecurrentSchema

    def __init__(self,
                 return_sequences=False,
                 return_state=False,
                 go_backwards=False,
                 stateful=False,
                 unroll=False,
                 implementation=0,
                 **kwargs):
        super(RecurrentConfig, self).__init__(**kwargs)
        self.return_sequences = return_sequences
        self.return_state = return_state
        self.go_backwards = go_backwards
        self.stateful = stateful
        self.unroll = unroll
        self.implementation = implementation


class SimpleRNNSchema(RecurrentSchema):
    units = fields.Int()
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    recurrent_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    recurrent_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    recurrent_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    bias_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    dropout = fields.Float(default=0., missing=0.)
    recurrent_dropout = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SimpleRNNConfig(**data)

    @post_dump
    def unmake(self, data):
        return SimpleRNNConfig.remove_reduced_attrs(data)


class SimpleRNNConfig(RecurrentConfig):
    """Fully-connected RNN where the output is to be fed back to input.

    Args:
        units: Positive integer, dimensionality of the output space.
        activation: Activation function to use.
            If you don't specify anything, no activation is applied
            If you pass None, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix,
            used for the linear transformation of the inputs..
        recurrent_initializer: Initializer for the `recurrent_kernel`
            weights matrix,
            used for the linear transformation of the recurrent state..
        bias_initializer: Initializer for the bias vector.
        kernel_regularizer: Regularizer function applied to
            the `kernel` weights matrix.
        recurrent_regularizer: Regularizer function applied to
            the `recurrent_kernel` weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to
            the `kernel` weights matrix.
        recurrent_constraint: Constraint function applied to
            the `recurrent_kernel` weights matrix.
        bias_constraint: Constraint function applied to the bias vector.
        dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the inputs.
        recurrent_dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the recurrent state.

    References:
        - [A Theoretically Grounded Application of Dropout in Recurrent Neural
          Networks](http://arxiv.org/abs/1512.05287)

    Polyaxonfile usage:

    ```yaml
    SimpleRNN:
      units: 3
      activation: tanh
    ```
    """
    IDENTIFIER = 'SimpleRNN'
    SCHEMA = SimpleRNNSchema

    def __init__(self,
                 units,
                 activation='tanh',
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 recurrent_initializer=OrthogonalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(SimpleRNNConfig, self).__init__(**kwargs)
        self.units = units
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.recurrent_initializer = recurrent_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.recurrent_regularizer = recurrent_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.recurrent_constraint = recurrent_constraint
        self.bias_constraint = bias_constraint
        self.dropout = dropout
        self.recurrent_dropout = recurrent_dropout


class GRUSchema(RecurrentSchema):
    units = fields.Int()
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    recurrent_activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    recurrent_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    recurrent_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    recurrent_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    bias_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    dropout = fields.Float(default=0., missing=0.)
    recurrent_dropout = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GRUConfig(**data)

    @post_dump
    def unmake(self, data):
        return GRUConfig.remove_reduced_attrs(data)


class GRUConfig(RecurrentConfig):
    """Gated Recurrent Unit - Cho et al.

    2014.

    Args:
        units: Positive integer, dimensionality of the output space.
        activation: Activation function to use.
            If you pass None, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        recurrent_activation: Activation function to use
            for the recurrent step.
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix,
            used for the linear transformation of the inputs..
        recurrent_initializer: Initializer for the `recurrent_kernel`
            weights matrix,
            used for the linear transformation of the recurrent state..
        bias_initializer: Initializer for the bias vector.
        kernel_regularizer: Regularizer function applied to
            the `kernel` weights matrix.
        recurrent_regularizer: Regularizer function applied to
            the `recurrent_kernel` weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to
            the `kernel` weights matrix.
        recurrent_constraint: Constraint function applied to
            the `recurrent_kernel` weights matrix.
        bias_constraint: Constraint function applied to the bias vector.
        dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the inputs.
        recurrent_dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the recurrent state.

    References:
        - [On the Properties of Neural Machine Translation: Encoder-Decoder
          Approaches](https://arxiv.org/abs/1409.1259)
        - [Empirical Evaluation of Gated Recurrent Neural Networks on Sequence
          Modeling](http://arxiv.org/abs/1412.3555v1)
        - [A Theoretically Grounded Application of Dropout in Recurrent Neural
          Networks](http://arxiv.org/abs/1512.05287)

    Polyaxonfile usage:

    ```yaml
    GRU:
      units: 3
      activation: tanh
    ```
    """
    IDENTIFIER = 'GRU'
    SCHEMA = GRUSchema

    def __init__(self,
                 units,
                 activation='tanh',
                 recurrent_activation='hard_sigmoid',
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 recurrent_initializer=OrthogonalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(GRUConfig, self).__init__(**kwargs)
        self.units = units
        self.activation = activation
        self.recurrent_activation = recurrent_activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.recurrent_initializer = recurrent_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.recurrent_regularizer = recurrent_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.recurrent_constraint = recurrent_constraint
        self.bias_constraint = bias_constraint
        self.dropout = dropout
        self.recurrent_dropout = recurrent_dropout


class LSTMSchema(RecurrentSchema):
    units = fields.Int()
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    recurrent_activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    recurrent_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    unit_forget_bias = fields.Bool(default=True, missing=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    recurrent_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    recurrent_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    bias_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    dropout = fields.Float(default=0., missing=0.)
    recurrent_dropout = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LSTMConfig(**data)

    @post_dump
    def unmake(self, data):
        return LSTMConfig.remove_reduced_attrs(data)


class LSTMConfig(RecurrentConfig):
    """Long-Short Term Memory unit - Hochreiter 1997.

    For a step-by-step description of the algorithm, see
    [this tutorial](http://deeplearning.net/tutorial/lstm.html).

    Args:
        units: Positive integer, dimensionality of the output space.
        activation: Activation function to use.
            If you pass None, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        recurrent_activation: Activation function to use
            for the recurrent step.
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix,
            used for the linear transformation of the inputs..
        recurrent_initializer: Initializer for the `recurrent_kernel`
            weights matrix,
            used for the linear transformation of the recurrent state..
        bias_initializer: Initializer for the bias vector.
        unit_forget_bias: Boolean.
            If True, add 1 to the bias of the forget gate at initialization.
            Setting it to true will also force `bias_initializer="zeros"`.
            This is recommended in [Jozefowicz et
              al.](http://www.jmlr.org/proceedings/papers/v37/jozefowicz15.pdf)
        kernel_regularizer: Regularizer function applied to
            the `kernel` weights matrix.
        recurrent_regularizer: Regularizer function applied to
            the `recurrent_kernel` weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to
            the `kernel` weights matrix.
        recurrent_constraint: Constraint function applied to
            the `recurrent_kernel` weights matrix.
        bias_constraint: Constraint function applied to the bias vector.
        dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the inputs.
        recurrent_dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the recurrent state.

    References:
        - [Long short-term
          memory]((http://www.bioinf.jku.at/publications/older/2604.pdf)
          (original 1997 paper)
        - [Supervised sequence labeling with recurrent neural
          networks](http://www.cs.toronto.edu/~graves/preprint.pdf)
        - [A Theoretically Grounded Application of Dropout in Recurrent Neural
          Networks](http://arxiv.org/abs/1512.05287)

    Polyaxonfile usage:

    ```yaml
    LSTM:
      units: 3
      activation: tanh
    ```
    """
    IDENTIFIER = 'LSTM'
    SCHEMA = LSTMSchema

    def __init__(self,
                 units,
                 activation='tanh',
                 recurrent_activation='hard_sigmoid',
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 recurrent_initializer=OrthogonalInitializerConfig,
                 bias_initializer=ZerosInitializerConfig(),
                 unit_forget_bias=True,
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(LSTMConfig, self).__init__(**kwargs)
        self.units = units
        self.activation = activation
        self.recurrent_activation = recurrent_activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.recurrent_initializer = recurrent_initializer
        self.bias_initializer = bias_initializer
        self.unit_forget_bias = unit_forget_bias
        self.kernel_regularizer = kernel_regularizer
        self.recurrent_regularizer = recurrent_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.recurrent_constraint = recurrent_constraint
        self.bias_constraint = bias_constraint
        self.dropout = dropout
        self.recurrent_dropout = recurrent_dropout
