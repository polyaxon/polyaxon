# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate, post_load

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import (
    InitializerSchema,
    ZerosInitializerConfig,
    OrthogonalInitializerConfig,
    GlorotUniformInitializerConfig,
)
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig
from polyaxon_schemas.utils import StrOrFct, ACTIVATION_VALUES


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
    def make_load(self, data):
        return RecurrentConfig(**data)


class RecurrentConfig(BaseLayerConfig):
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
    def make_load(self, data):
        return SimpleRNNConfig(**data)


class SimpleRNNConfig(RecurrentConfig):
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
    def make_load(self, data):
        return GRUConfig(**data)


class GRUConfig(RecurrentConfig):
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
    def make_load(self, data):
        return LSTMConfig(**data)


class LSTMConfig(RecurrentConfig):
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
