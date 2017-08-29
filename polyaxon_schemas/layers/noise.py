# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate, post_load

from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class GaussianNoiseSchema(BaseLayerSchema):
    stddev = fields.Float()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GaussianNoiseConfig(**data)


class GaussianNoiseConfig(BaseLayerConfig):
    IDENTIFIER = 'GaussianNoise'
    SCHEMA = GaussianNoiseSchema

    def __init__(self, stddev, **kwargs):
        super(GaussianNoiseConfig, self).__init__(**kwargs)
        self.stddev = stddev


class GaussianDropoutSchema(BaseLayerSchema):
    rate = fields.Float(validate=validate.Range(0, 1))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GaussianDropoutConfig(**data)


class GaussianDropoutConfig(BaseLayerConfig):
    IDENTIFIER = 'GaussianDropout'
    SCHEMA = GaussianDropoutSchema

    def __init__(self, rate, **kwargs):
        super(GaussianDropoutConfig, self).__init__(**kwargs)
        self.rate = rate


class AlphaDropoutSchema(BaseLayerSchema):
    rate = fields.Float(validate=validate.Range(0, 1))
    noise_shape = fields.List(fields.Int, default=None, missing=None)
    seed = fields.Int(default=None, missing=None)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AlphaDropoutConfig(**data)


class AlphaDropoutConfig(BaseLayerConfig):
    IDENTIFIER = 'AlphaDropout'
    SCHEMA = AlphaDropoutSchema

    def __init__(self, rate, noise_shape=None, seed=None, **kwargs):
        super(AlphaDropoutConfig, self).__init__(**kwargs)
        self.rate = rate
        self.noise_shape = noise_shape
        self.seed = seed
