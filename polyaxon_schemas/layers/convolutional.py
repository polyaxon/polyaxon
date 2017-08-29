# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load, validate

from polyaxon_schemas.utils import ObjectOrListObject, StrOrFct, ACTIVATION_VALUES
from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import (
    InitializerSchema,
    GlorotNormalInitializerConfig,
    ZerosInitializerConfig,
)
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class Conv1DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=1, max=1)
    strides = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    dilation_rate = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Conv1DConfig(**data)


class Conv1DConfig(BaseLayerConfig):
    IDENTIFIER = 'Conv1D'
    SCHEMA = Conv1DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=1,
                 padding='valid',
                 dilation_rate=1,
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv1DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.dilation_rate = dilation_rate
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv2DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Conv2DConfig(**data)


class Conv2DConfig(BaseLayerConfig):
    IDENTIFIER = 'Conv2D'
    SCHEMA = Conv2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.dilation_rate = dilation_rate
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv3DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=3, max=3)
    strides = ObjectOrListObject(fields.Int, min=3, max=3, default=(1, 1, 1), missing=(1, 1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=3, max=3,
                                       default=(1, 1, 1), missing=(1, 1, 1))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Conv3DConfig(**data)


class Conv3DConfig(BaseLayerConfig):
    IDENTIFIER = 'Conv3D'
    SCHEMA = Conv3DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv3DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.dilation_rate = dilation_rate
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv2DTransposeSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Conv2DTransposeConfig(**data)


class Conv2DTransposeConfig(BaseLayerConfig):
    IDENTIFIER = 'Conv2DTranspose'
    SCHEMA = Conv2DTransposeSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv2DTransposeConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.dilation_rate = dilation_rate
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv3DTransposeSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=3, max=3)
    strides = ObjectOrListObject(fields.Int, min=3, max=3, default=(1, 1, 1), missing=(1, 1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    dilation_rate = ObjectOrListObject(fields.Int, min=3, max=3,
                                       default=(1, 1, 1), missing=(1, 1, 1))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Conv3DTransposeConfig(**data)


class Conv3DTransposeConfig(BaseLayerConfig):
    IDENTIFIER = 'Conv3DTranspose'
    SCHEMA = Conv3DTransposeSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1, 1),
                 padding='valid',
                 data_format=None,
                 activation=None,
                 dilation_rate=(1, 1, 1),
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv3DTransposeConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.dilation_rate = dilation_rate
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class SeparableConv2DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    depth_multiplier = fields.Int(default=1, missing=1)
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    depthwise_initializer = fields.Nested(InitializerSchema, allow_none=True)
    pointwise_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    depthwise_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    pointwise_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    depthwise_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    pointwise_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SeparableConv2DConfig(**data)


class SeparableConv2DConfig(BaseLayerConfig):
    IDENTIFIER = 'SeparableConv2D'
    SCHEMA = SeparableConv2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 depth_multiplier=1,
                 activation=None,
                 use_bias=True,
                 depthwise_initializer=GlorotNormalInitializerConfig(),
                 pointwise_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 depthwise_regularizer=None,
                 pointwise_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 depthwise_constraint=None,
                 pointwise_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(SeparableConv2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.depth_multiplier = depth_multiplier
        self.activation = activation
        self.use_bias = use_bias
        self.depthwise_initializer = depthwise_initializer
        self.pointwise_initializer = pointwise_initializer
        self.bias_initializer = bias_initializer
        self.depthwise_regularizer = depthwise_regularizer
        self.pointwise_regularizer = pointwise_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.depthwise_constraint = depthwise_constraint
        self.pointwise_constraint = pointwise_constraint
        self.bias_constraint = bias_constraint


class UpSampling1DSchema(BaseLayerSchema):
    size = ObjectOrListObject(fields.Int, min=2, max=2, default=2, missing=2)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return UpSampling1DConfig(**data)


class UpSampling1DConfig(BaseLayerConfig):
    IDENTIFIER = 'UpSampling1D'
    SCHEMA = UpSampling1DSchema

    def __init__(self, size=2, **kwargs):
        super(UpSampling1DConfig, self).__init__(**kwargs)
        self.size = size


class UpSampling2DSchema(BaseLayerSchema):
    size = ObjectOrListObject(fields.Int, min=2, max=2, default=(2, 2), missing=(2, 2))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return UpSampling2DConfig(**data)


class UpSampling2DConfig(BaseLayerConfig):
    IDENTIFIER = 'UpSampling2D'
    SCHEMA = UpSampling2DSchema

    def __init__(self, size=(2, 2), data_format=None, **kwargs):
        super(UpSampling2DConfig, self).__init__(**kwargs)
        self.size = size
        self.data_format = data_format


class UpSampling3DSchema(BaseLayerSchema):
    size = ObjectOrListObject(fields.Int, min=3, max=3, default=(2, 2, 2), missing=(2, 2, 2))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return UpSampling3DConfig(**data)


class UpSampling3DConfig(BaseLayerConfig):
    IDENTIFIER = 'UpSampling3D'
    SCHEMA = UpSampling3DSchema

    def __init__(self, size=(2, 2, 2), data_format=None, **kwargs):
        super(UpSampling3DConfig, self).__init__(**kwargs)
        self.size = size
        self.data_format = data_format


class ZeroPadding1DSchema(BaseLayerSchema):
    padding = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ZeroPadding1DConfig(**data)


class ZeroPadding1DConfig(BaseLayerConfig):
    IDENTIFIER = 'ZeroPadding1D'
    SCHEMA = ZeroPadding1DSchema

    def __init__(self, padding=1, **kwargs):
        super(ZeroPadding1DConfig, self).__init__(**kwargs)
        self.padding = padding


class ZeroPadding2DSchema(BaseLayerSchema):
    padding = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ZeroPadding2DConfig(**data)


class ZeroPadding2DConfig(BaseLayerConfig):
    IDENTIFIER = 'ZeroPadding2D'
    SCHEMA = ZeroPadding2DSchema

    def __init__(self, padding=(1, 1), data_format=None, **kwargs):
        super(ZeroPadding2DConfig, self).__init__(**kwargs)
        self.padding = padding
        self.data_format = data_format


class ZeroPadding3DSchema(BaseLayerSchema):
    padding = ObjectOrListObject(fields.Int, min=3, max=3, default=(1, 1, 1), missing=(1, 1, 1))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ZeroPadding3DConfig(**data)


class ZeroPadding3DConfig(BaseLayerConfig):
    IDENTIFIER = 'ZeroPadding3D'
    SCHEMA = ZeroPadding3DSchema

    def __init__(self, padding=(1, 1, 1), data_format=None, **kwargs):
        super(ZeroPadding3DConfig, self).__init__(**kwargs)
        self.padding = padding
        self.data_format = data_format


class Cropping1DSchema(BaseLayerSchema):
    cropping = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Cropping1DConfig(**data)


class Cropping1DConfig(BaseLayerConfig):
    IDENTIFIER = 'Cropping1D'
    SCHEMA = Cropping1DSchema

    def __init__(self, cropping=(1, 1), **kwargs):
        super(Cropping1DConfig, self).__init__(**kwargs)
        self.cropping = cropping


class Cropping2DSchema(BaseLayerSchema):
    cropping = ObjectOrListObject(ObjectOrListObject(fields.Int, min=2, max=2), min=2, max=2,
                                  default=((0, 0), (0, 0)), missing=((0, 0), (0, 0)))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Cropping2DConfig(**data)


class Cropping2DConfig(BaseLayerConfig):
    IDENTIFIER = 'Cropping2D'
    SCHEMA = Cropping2DSchema

    def __init__(self, cropping=((0, 0), (0, 0)), data_format=None, **kwargs):
        super(Cropping2DConfig, self).__init__(**kwargs)
        self.cropping = cropping
        self.data_format = data_format


class Cropping3DSchema(BaseLayerSchema):
    cropping = ObjectOrListObject(ObjectOrListObject(fields.Int, min=2, max=2), min=3, max=3,
                                  default=((1, 1), (1, 1), (1, 1)),
                                  missing=((1, 1), (1, 1), (1, 1)))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Cropping3DConfig(**data)


class Cropping3DConfig(BaseLayerConfig):
    IDENTIFIER = 'Cropping3D'
    SCHEMA = Cropping3DSchema

    def __init__(self, cropping=((1, 1), (1, 1), (1, 1)), data_format=None, **kwargs):
        super(Cropping3DConfig, self).__init__(**kwargs)
        self.cropping = cropping
        self.data_format = data_format
