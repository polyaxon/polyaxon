# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, validate

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.utils import DType


class ZerosInitializerSchema(Schema):
    dtype = DType(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ZerosInitializerConfig(**data)


class ZerosInitializerConfig(BaseConfig):
    IDENTIFIER = 'Zeros'
    SCHEMA = ZerosInitializerSchema

    def __init__(self, dtype='float32'):
        self.dtype = dtype


class OnesInitializerSchema(Schema):
    dtype = DType(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return OnesInitializerConfig(**data)


class OnesInitializerConfig(BaseConfig):
    IDENTIFIER = 'Ones'
    SCHEMA = OnesInitializerSchema

    def __init__(self, dtype='float32'):
        self.dtype = dtype


class ConstantInitializerSchema(Schema):
    value = fields.Int(allow_none=True)
    dtype = DType(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ConstantInitializerConfig(**data)


class ConstantInitializerConfig(BaseConfig):
    IDENTIFIER = 'Constant'
    SCHEMA = ConstantInitializerSchema

    def __init__(self, value=0, dtype='float32'):
        self.dtype = dtype
        self.value = value


class UniformInitializerSchema(Schema):
    minval = fields.Number(allow_none=True)
    maxval = fields.Number(allow_none=True)
    dtype = DType(allow_none=True)
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return UniformInitializerConfig(**data)


class UniformInitializerConfig(BaseConfig):
    IDENTIFIER = 'Uniform'
    SCHEMA = UniformInitializerSchema

    def __init__(self, minval=0, maxval=None, seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.minval = minval
        self.maxval = maxval


class NormalInitializerSchema(Schema):
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)
    dtype = DType(allow_none=True)
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return NormalInitializerConfig(**data)


class NormalInitializerConfig(BaseConfig):
    IDENTIFIER = 'Normal'
    SCHEMA = NormalInitializerSchema

    def __init__(self, mean=0., stddev=1., seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.mean = mean
        self.stddev = stddev


class TruncatedNormalInitializerSchema(Schema):
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TruncatedNormalInitializerConfig(**data)


class TruncatedNormalInitializerConfig(BaseConfig):
    IDENTIFIER = 'TruncatedNormal'
    SCHEMA = TruncatedNormalInitializerSchema

    def __init__(self, mean=0., stddev=1., seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.mean = mean
        self.stddev = stddev


class VarianceScalingInitializerSchema(Schema):
    scale = fields.Float(allow_none=True)
    mode = fields.Str(allow_none=True, validate=validate.OneOf(['fan_in', 'fan_out', 'fan_avg']))
    distribution = fields.Str(allow_none=True)
    dtype = DType(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return VarianceScalingInitializerConfig(**data)


class VarianceScalingInitializerConfig(BaseConfig):
    IDENTIFIER = 'VarianceScaling'
    SCHEMA = VarianceScalingInitializerSchema

    def __init__(self, scale=1., mode='fan_in', distribution="normal", dtype='float32'):
        self.scale = scale
        self.mode = mode
        self.distribution = distribution
        self.dtype = dtype


class IdentityInitializerSchema(Schema):
    gain = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return IdentityInitializerConfig(**data)


class IdentityInitializerConfig(BaseConfig):
    IDENTIFIER = 'Identity'
    SCHEMA = IdentityInitializerSchema

    def __init__(self, gain=1.):
        self.gain = gain


class OrthogonalInitializerSchema(Schema):
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)
    gain = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return OrthogonalInitializerConfig(**data)


class OrthogonalInitializerConfig(BaseConfig):
    IDENTIFIER = 'Orthogonal'
    SCHEMA = OrthogonalInitializerSchema

    def __init__(self, gain=1., seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.gain = gain


class GlorotUniformInitializerSchema(Schema):
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlorotUniformInitializerConfig(**data)


class GlorotUniformInitializerConfig(BaseConfig):
    IDENTIFIER = 'GlorotUniform'
    SCHEMA = GlorotUniformInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class GlorotNormalInitializerSchema(Schema):
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlorotNormalInitializerConfig(**data)


class GlorotNormalInitializerConfig(BaseConfig):
    IDENTIFIER = 'GlorotNormal'
    SCHEMA = GlorotNormalInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class HeUniformInitializerSchema(Schema):
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return HeUniformInitializerConfig(**data)


class HeUniformInitializerConfig(BaseConfig):
    IDENTIFIER = 'HeUniform'
    SCHEMA = HeUniformInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class HeNormalInitializerSchema(Schema):
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return HeNormalInitializerConfig(**data)


class HeNormalInitializerConfig(BaseConfig):
    IDENTIFIER = 'HeNormal'
    SCHEMA = HeNormalInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class LecunUniformInitializerSchema(Schema):
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LecunUniformInitializerConfig(**data)


class LecunUniformInitializerConfig(BaseConfig):
    IDENTIFIER = 'LecunUniform'
    SCHEMA = LecunUniformInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class LecunNormalInitializerSchema(Schema):
    seed = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LecunNormalInitializerConfig(**data)


class LecunNormalInitializerConfig(BaseConfig):
    IDENTIFIER = 'LecunNormal'
    SCHEMA = LecunNormalInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class InitializerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'initializer'
    __configs__ = {
        ZerosInitializerConfig.IDENTIFIER: ZerosInitializerConfig,
        OnesInitializerConfig.IDENTIFIER: OnesInitializerConfig,
        ConstantInitializerConfig.IDENTIFIER: ConstantInitializerConfig,
        UniformInitializerConfig.IDENTIFIER: UniformInitializerConfig,
        NormalInitializerConfig.IDENTIFIER: NormalInitializerConfig,
        TruncatedNormalInitializerConfig.IDENTIFIER: TruncatedNormalInitializerConfig,
        VarianceScalingInitializerConfig.IDENTIFIER: VarianceScalingInitializerConfig,
        IdentityInitializerConfig.IDENTIFIER: IdentityInitializerConfig,
        OrthogonalInitializerConfig.IDENTIFIER: OrthogonalInitializerConfig,
        GlorotUniformInitializerConfig.IDENTIFIER: GlorotUniformInitializerConfig,
        GlorotNormalInitializerConfig.IDENTIFIER: GlorotNormalInitializerConfig,
        HeUniformInitializerConfig.IDENTIFIER: HeUniformInitializerConfig,
        HeNormalInitializerConfig.IDENTIFIER: HeNormalInitializerConfig,
        LecunUniformInitializerConfig.IDENTIFIER: LecunUniformInitializerConfig,
        LecunNormalInitializerConfig.IDENTIFIER: LecunNormalInitializerConfig,
    }
    __support_snake_case__ = True
