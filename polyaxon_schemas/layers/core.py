# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load, validate

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import (
    InitializerSchema,
    GlorotNormalInitializerConfig,
    ZerosInitializerConfig,
)
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig
from polyaxon_schemas.utils import StrOrFct, DType, ACTIVATION_VALUES


class MaskingSchema(BaseLayerSchema):
    mask_value = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MaskingConfig(**data)


class MaskingConfig(BaseLayerConfig):
    IDENTIFIER = 'Masking'
    SCHEMA = MaskingSchema

    def __init__(self, mask_value=0., **kwargs):
        super(MaskingConfig, self).__init__(**kwargs)
        self.mask_value = mask_value


class DropoutSchema(BaseLayerSchema):
    rate = fields.Float(validate=validate.Range(0, 1))
    noise_shape = fields.List(fields.Int, default=None, missing=None)
    seed = fields.Int(default=None, missing=None)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return DropoutConfig(**data)


class DropoutConfig(BaseLayerConfig):
    IDENTIFIER = 'Dropout'
    SCHEMA = DropoutSchema

    def __init__(self, rate, noise_shape=None, seed=None, **kwargs):
        super(DropoutConfig, self).__init__(**kwargs)
        self.rate = rate
        self.noise_shape = noise_shape
        self.seed = seed


class SpatialDropout1DSchema(DropoutSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SpatialDropout1DConfig(**data)


class SpatialDropout1DConfig(DropoutConfig):
    IDENTIFIER = 'SpatialDropout1D'
    SCHEMA = SpatialDropout1DSchema


class SpatialDropout2DSchema(DropoutSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SpatialDropout2DConfig(**data)


class SpatialDropout2DConfig(DropoutConfig):
    IDENTIFIER = 'SpatialDropout2D'
    SCHEMA = SpatialDropout2DSchema

    def __init__(self, rate, data_format=None, **kwargs):
        super(SpatialDropout2DConfig, self).__init__(rate, **kwargs)
        self.data_format = data_format


class SpatialDropout3DSchema(DropoutSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SpatialDropout3DConfig(**data)


class SpatialDropout3DConfig(DropoutConfig):
    IDENTIFIER = 'SpatialDropout3D'
    SCHEMA = SpatialDropout3DSchema

    def __init__(self, rate, data_format=None, **kwargs):
        super(SpatialDropout3DConfig, self).__init__(rate, **kwargs)
        self.data_format = data_format


class ActivationSchema(BaseLayerSchema):
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ActivationConfig(**data)


class ActivationConfig(BaseLayerConfig):
    IDENTIFIER = 'Activation'
    SCHEMA = ActivationSchema

    def __init__(self, activation, **kwargs):
        super(ActivationConfig, self).__init__(**kwargs)
        self.activation = activation


class ReshapeSchema(BaseLayerSchema):
    target_shape = fields.List(fields.Int)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ReshapeConfig(**data)


class ReshapeConfig(BaseLayerConfig):
    IDENTIFIER = 'Reshape'
    SCHEMA = ReshapeSchema

    def __init__(self, target_shape, **kwargs):
        super(ReshapeConfig, self).__init__(**kwargs)
        self.target_shape = target_shape


class PermuteSchema(BaseLayerSchema):
    dims = fields.List(fields.Int)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PermuteConfig(**data)


class PermuteConfig(BaseLayerConfig):
    IDENTIFIER = 'Permute'
    SCHEMA = PermuteSchema

    def __init__(self, dims, **kwargs):
        super(PermuteConfig, self).__init__(**kwargs)
        self.dims = dims


class FlattenSchema(BaseLayerSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return FlattenConfig(**data)


class FlattenConfig(BaseLayerConfig):
    IDENTIFIER = 'Flatten'
    SCHEMA = FlattenSchema


class RepeatVectorSchema(BaseLayerSchema):
    n = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return RepeatVectorConfig(**data)


class RepeatVectorConfig(BaseLayerConfig):
    IDENTIFIER = 'RepeatVector'
    SCHEMA = RepeatVectorSchema

    def __init__(self, n, **kwargs):
        super(RepeatVectorConfig, self).__init__(**kwargs)
        self.n = n


# class LambdaSchema(BaseLayerSchema):


class DenseSchema(BaseLayerSchema):
    units = fields.Int()
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(allow_none=True)
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
        return DenseConfig(**data)


class DenseConfig(BaseLayerConfig):
    IDENTIFIER = 'Dense'
    SCHEMA = DenseSchema

    def __init__(self,
                 units,
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
        super(DenseConfig, self).__init__(**kwargs)
        self.units = units
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class ActivityRegularizationSchema(BaseLayerSchema):
    l1 = fields.Float(allow_none=True)
    l2 = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ActivityRegularizationConfig(**data)


class ActivityRegularizationConfig(BaseLayerConfig):
    IDENTIFIER = 'ActivityRegularization'
    SCHEMA = ActivityRegularizationSchema

    def __init__(self, l1=0., l2=0., **kwargs):
        super(ActivityRegularizationConfig, self).__init__(**kwargs)
        self.l1 = l1
        self.l2 = l2


class CastSchema(BaseLayerSchema):
    dtype = DType()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return CastConfig(**data)


class CastConfig(BaseLayerConfig):
    IDENTIFIER = 'Cast'
    SCHEMA = CastSchema

    def __init__(self, dtype, **kwargs):
        super(CastConfig, self).__init__(**kwargs)
        self.dtype = dtype
