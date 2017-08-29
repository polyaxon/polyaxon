# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load, validate

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import InitializerSchema
from polyaxon_schemas.layers.recurrent import RecurrentSchema, RecurrentConfig
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.utils import ObjectOrListObject, ACTIVATION_VALUES


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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ConvRecurrent2DConfig(**data)


class ConvRecurrent2DConfig(RecurrentConfig):
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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ConvLSTM2DConfig(**data)


class ConvLSTM2DConfig(ConvRecurrent2DConfig):
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
