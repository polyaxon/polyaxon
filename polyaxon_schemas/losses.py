# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.utils import Tensor


class BaseLossSchema(Schema):
    input_layer = Tensor(allow_none=True)
    output_layer = Tensor(allow_none=True)
    weights = fields.Float(default=1.0, missing=1.0)
    name = fields.Str(allow_none=True)
    collect = fields.Bool(default=True, missing=True)


class BaseLossConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['input_layer', 'output_layer', 'name']

    def __init__(self, input_layer=None, output_layer=None, weights=1.0, name=None, collect=True):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.weights = weights
        self.name = name
        self.collect = collect


class AbsoluteDifferenceSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AbsoluteDifferenceConfig(**data)


class AbsoluteDifferenceConfig(BaseLossConfig):
    IDENTIFIER = 'AbsoluteDifference'
    SCHEMA = AbsoluteDifferenceSchema


class MeanSquaredErrorSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanSquaredErrorConfig(**data)


class MeanSquaredErrorConfig(BaseLossConfig):
    IDENTIFIER = 'MeanSquaredError'
    SCHEMA = MeanSquaredErrorSchema


class LogLossSchema(BaseLossSchema):
    epsilon = fields.Float(default=1e-7, missing=1e-7)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LogLossConfig(**data)


class LogLossConfig(BaseLossConfig):
    IDENTIFIER = 'LogLoss'
    SCHEMA = LogLossSchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 epsilon=1e-7,
                 name=None,
                 collect=True):
        super(LogLossConfig, self).__init__(input_layer, output_layer, weights, name, collect)
        self.epsilon = epsilon


class HuberLossSchema(BaseLossSchema):
    clip = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return HuberLossConfig(**data)


class HuberLossConfig(BaseLossConfig):
    IDENTIFIER = 'HuberLoss'
    SCHEMA = HuberLossSchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 clip=0.,
                 name=None,
                 collect=True):
        super(HuberLossConfig, self).__init__(input_layer, output_layer, weights, name, collect)
        self.clip = clip


class ClippedDeltaLossSchema(BaseLossSchema):
    clip_value_min = fields.Float(default=-1., missing=-1.)
    clip_value_max = fields.Float(default=-1., missing=-1.)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ClippedDeltaLossConfig(**data)


class ClippedDeltaLossConfig(BaseLossConfig):
    IDENTIFIER = 'ClippedDeltaLoss'
    SCHEMA = ClippedDeltaLossSchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 clip_value_min=-1.,
                 clip_value_max=1.,
                 name=None,
                 collect=True):
        super(ClippedDeltaLossConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)
        self.clip_value_min = clip_value_min
        self.clip_value_max = clip_value_max


class SoftmaxCrossEntropySchema(BaseLossSchema):
    label_smoothing = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SoftmaxCrossEntropyConfig(**data)


class SoftmaxCrossEntropyConfig(BaseLossConfig):
    IDENTIFIER = 'SoftmaxCrossEntropy'
    SCHEMA = SoftmaxCrossEntropySchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 label_smoothing=0.,
                 name=None,
                 collect=True):
        super(SoftmaxCrossEntropyConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)
        self.label_smoothing = label_smoothing


class SigmoidCrossEntropySchema(BaseLossSchema):
    label_smoothing = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SigmoidCrossEntropyConfig(**data)


class SigmoidCrossEntropyConfig(BaseLossConfig):
    IDENTIFIER = 'SigmoidCrossEntropy'
    SCHEMA = SigmoidCrossEntropySchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 label_smoothing=0.,
                 name=None,
                 collect=True):
        super(SigmoidCrossEntropyConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)
        self.label_smoothing = label_smoothing


class HingeLossSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return HingeLossConfig(**data)


class HingeLossConfig(BaseLossConfig):
    IDENTIFIER = 'HingeLoss'
    SCHEMA = HingeLossSchema


class CosineDistanceSchema(BaseLossSchema):
    dim = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return CosineDistanceConfig(**data)


class CosineDistanceConfig(BaseLossConfig):
    IDENTIFIER = 'CosineDistance'
    SCHEMA = CosineDistanceSchema

    def __init__(self,
                 dim,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 name=None,
                 collect=True):
        self.dim = dim
        super(CosineDistanceConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)


class PoissonLossSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PoissonLossConfig(**data)


class PoissonLossConfig(BaseLossConfig):
    IDENTIFIER = 'PoissonLoss'
    SCHEMA = PoissonLossSchema


class KullbackLeiberDivergenceSchema(BaseLossSchema):
    dim = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return KullbackLeiberDivergenceConfig(**data)


class KullbackLeiberDivergenceConfig(BaseLossConfig):
    IDENTIFIER = 'KullbackLeiberDivergence'
    SCHEMA = KullbackLeiberDivergenceSchema

    def __init__(self,
                 dim,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0, name='KullbackLeiberDivergence',
                 collect=True):
        self.dim = dim
        super(KullbackLeiberDivergenceConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)


class LossSchema(BaseMultiSchema):
    __multi_schema_name__ = 'loss'
    __configs__ = {
        AbsoluteDifferenceConfig.IDENTIFIER: AbsoluteDifferenceConfig,
        MeanSquaredErrorConfig.IDENTIFIER: MeanSquaredErrorConfig,
        LogLossConfig.IDENTIFIER: LogLossConfig,
        HuberLossConfig.IDENTIFIER: HuberLossConfig,
        ClippedDeltaLossConfig.IDENTIFIER: ClippedDeltaLossConfig,
        SoftmaxCrossEntropyConfig.IDENTIFIER: SoftmaxCrossEntropyConfig,
        SigmoidCrossEntropyConfig.IDENTIFIER: SigmoidCrossEntropyConfig,
        HingeLossConfig.IDENTIFIER: HingeLossConfig,
        CosineDistanceConfig.IDENTIFIER: CosineDistanceConfig,
        KullbackLeiberDivergenceConfig.IDENTIFIER: KullbackLeiberDivergenceConfig,
    }
