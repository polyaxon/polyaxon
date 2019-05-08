# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.fields import ObjectOrListObject
from polyaxon_schemas.ml.constraints import ConstraintSchema
from polyaxon_schemas.ml.initializations import InitializerSchema
from polyaxon_schemas.ml.layers.recurrent import RecurrentConfig, RecurrentSchema
from polyaxon_schemas.ml.regularizations import RegularizerSchema
from polyaxon_schemas.ml.utils import ACTIVATION_VALUES


class ConvRecurrent2DSchema(RecurrentSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(allow_none=True,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    return_sequences = fields.Bool(default=False, missing=False)
    go_backwards = fields.Bool(default=False, missing=False)
    stateful = fields.Bool(default=False, missing=False)

    @staticmethod
    def schema_config():
        return ConvRecurrent2DConfig


class ConvRecurrent2DConfig(RecurrentConfig):
    """Abstract base class for convolutional recurrent layers.

    Do not use in a model -- it's not a functional layer!

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number output of filters in the convolution).
        kernel_size: An integer or tuple/list of n integers, specifying the
            dimensions of the convolution window.
        strides: An integer or tuple/list of n integers,
            specifying the strides of the convolution.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: One of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, time, ..., channels)`
            while `channels_first` corresponds to
            inputs with shape `(batch, time, channels, ...)`.
            If you never set it, then it will be "channels_last".
        dilation_rate: An integer or tuple/list of n integers, specifying
            the dilation rate to use for dilated convolution.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any `strides` value != 1.
        return_sequences: Boolean. Whether to return the last output
            in the output sequence, or the full sequence.
        go_backwards: Boolean (default False).
            If True, rocess the input sequence backwards.
        stateful: Boolean (default False). If True, the last state
            for each sample at index i in a batch will be used as initial
            state for the sample of index i in the following batch.

    Input shape:
        5D tensor with shape `(num_samples, timesteps, channels, rows, cols)`.

    Output shape:
        - if `return_sequences`: 5D tensor with shape
            `(num_samples, timesteps, channels, rows, cols)`.
        - else, 4D tensor with shape `(num_samples, channels, rows, cols)`.

    # Masking
        This layer supports masking for input data with a variable number
        of timesteps. To introduce masks to your data,
        use an `Embedding` layer with the `mask_zero` parameter
        set to `True`.
        **Note:** for the time being, masking is only supported with Theano.

    # Note on using statefulness in RNNs
        You can set RNN layers to be 'stateful', which means that the states
        computed for the samples in one batch will be reused as initial states
        for the samples in the next batch.
        This assumes a one-to-one mapping between
        samples in different successive batches.

        To enable statefulness:
            - specify `stateful=True` in the layer constructor.
            - specify a fixed batch size for your model, by passing
                a `batch_input_size=(...)` to the first layer in your model.
                This is the expected shape of your inputs *including the batch
                size*.
                It should be a tuple of integers, e.g. `(32, 10, 100)`.

        To reset the states of your model, call `.reset_states()` on either
        a specific layer, or on your entire model.
    """
    IDENTIFIER = 'ConvRecurrent2D'
    SCHEMA = ConvRecurrent2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 return_sequences=False,
                 go_backwards=False,
                 stateful=False,
                 **kwargs):
        super(ConvRecurrent2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.dilation_rate = dilation_rate
        self.return_sequences = return_sequences
        self.go_backwards = go_backwards
        self.stateful = stateful


class ConvLSTM2DSchema(ConvRecurrent2DSchema):
    activation = fields.Str(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    recurrent_activation = fields.Str(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    recurrent_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    unit_forget_bias = fields.Bool(default=True, missing=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    recurrent_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    recurrent_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    dropout = fields.Float(default=0., missing=0., validate=validate.Range(0., 1.))
    recurrent_dropout = fields.Float(default=0., missing=0., validate=validate.Range(0., 1.))

    @staticmethod
    def schema_config():
        return ConvLSTM2DConfig


class ConvLSTM2DConfig(ConvRecurrent2DConfig):
    """Convolutional LSTM.

    It is similar to an LSTM layer, but the input transformations
    and recurrent transformations are both convolutional.

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number output of filters in the convolution).
        kernel_size: An integer or tuple/list of n integers, specifying the
            dimensions of the convolution window.
        strides: An integer or tuple/list of n integers,
            specifying the strides of the convolution.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: One of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, time, ..., channels)`
            while `channels_first` corresponds to
            inputs with shape `(batch, time, channels, ...)`.
            If you never set it, then it will be "channels_last".
        dilation_rate: An integer or tuple/list of n integers, specifying
            the dilation rate to use for dilated convolution.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any `strides` value != 1.
        activation: Activation function to use.
            If you don't specify anything, no activation is applied
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
            Use in combination with `bias_initializer="zeros"`.
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
        return_sequences: Boolean. Whether to return the last output
            in the output sequence, or the full sequence.
        go_backwards: Boolean (default False).
            If True, rocess the input sequence backwards.
        stateful: Boolean (default False). If True, the last state
            for each sample at index i in a batch will be used as initial
            state for the sample of index i in the following batch.
        dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the inputs.
        recurrent_dropout: Float between 0 and 1.
            Fraction of the units to drop for
            the linear transformation of the recurrent state.

    Input shape:
        - if data_format='channels_first'
            5D tensor with shape:
            `(samples,time, channels, rows, cols)`
        - if data_format='channels_last'
            5D tensor with shape:
            `(samples,time, rows, cols, channels)`

    Output shape:
        - if `return_sequences`
             - if data_format='channels_first'
                5D tensor with shape:
                `(samples, time, filters, output_row, output_col)`
             - if data_format='channels_last'
                5D tensor with shape:
                `(samples, time, output_row, output_col, filters)`
        - else
            - if data_format ='channels_first'
                4D tensor with shape:
                `(samples, filters, output_row, output_col)`
            - if data_format='channels_last'
                4D tensor with shape:
                `(samples, output_row, output_col, filters)`
            where o_row and o_col depend on the shape of the filter and
            the padding

    Raises:
        ValueError: in case of invalid constructor arguments.

    References:
        - [Convolutional LSTM Network: A Machine Learning Approach for
        Precipitation Nowcasting](http://arxiv.org/abs/1506.04214v1)
        The current implementation does not include the feedback loop on the
        cells output

    Polyaxonfile usage:

    ```yaml
    ConvLSTM2D:
      filters: 3
      kernel_size: 2 or [2, 2]
      strides: 1 or [1, 1]
      padding: valid
    ```
    """
    IDENTIFIER = 'ConvLSTM2D'
    SCHEMA = ConvLSTM2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 activation='tanh',
                 recurrent_activation='hard_sigmoid',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 recurrent_initializer='orthogonal',
                 bias_initializer='zeros',
                 unit_forget_bias=True,
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 return_sequences=False,
                 go_backwards=False,
                 stateful=False,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(ConvLSTM2DConfig, self).__init__(
            filters,
            kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
            return_sequences=return_sequences,
            go_backwards=go_backwards,
            stateful=stateful,
            **kwargs)
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
