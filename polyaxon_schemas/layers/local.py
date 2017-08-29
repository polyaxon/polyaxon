# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load, validate

from polyaxon_schemas.utils import ObjectOrListObject, StrOrFct, ACTIVATION_VALUES
from polyaxon_schemas.initializations import (
    InitializerSchema,
    GlorotUniformInitializerConfig,
    ZerosInitializerConfig,
)
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class LocallyConnected1DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=1, max=1)
    strides = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LocallyConnected1DConfig(**data)


class LocallyConnected1DConfig(BaseLayerConfig):
    IDENTIFIER = 'LocallyConnected1D'
    SCHEMA = LocallyConnected1DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=1,
                 padding='valid',
                 data_format=None,
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(LocallyConnected1DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class LocallyConnected2DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LocallyConnected2DConfig(**data)


class LocallyConnected2DConfig(BaseLayerConfig):
    IDENTIFIER = 'LocallyConnected2D'
    SCHEMA = LocallyConnected2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(LocallyConnected2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint
