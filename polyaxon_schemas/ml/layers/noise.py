# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema


class GaussianNoiseSchema(BaseLayerSchema):
    stddev = fields.Float()

    @staticmethod
    def schema_config():
        return GaussianNoiseConfig


class GaussianNoiseConfig(BaseLayerConfig):
    """Apply additive zero-centered Gaussian noise.

    This is useful to mitigate overfitting
    (you could see it as a form of random data augmentation).
    Gaussian Noise (GS) is a natural choice as corruption process
    for real valued inputs.

    As it is a regularization layer, it is only active at training time.

    Args:
        stddev: float, standard deviation of the noise distribution.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as input.

    Polyaxonfile usage:

    ```yaml
    GaussianNoise:
      stddev: 0.5
    ```
    """
    IDENTIFIER = 'GaussianNoise'
    SCHEMA = GaussianNoiseSchema

    def __init__(self, stddev, **kwargs):
        super(GaussianNoiseConfig, self).__init__(**kwargs)
        self.stddev = stddev


class GaussianDropoutSchema(BaseLayerSchema):
    rate = fields.Float(validate=validate.Range(0, 1))

    @staticmethod
    def schema_config():
        return GaussianDropoutConfig


class GaussianDropoutConfig(BaseLayerConfig):
    """Apply multiplicative 1-centered Gaussian noise.

    As it is a regularization layer, it is only active at training time.

    Args:
        rate: float, drop probability (as with `Dropout`).
            The multiplicative noise will have
            standard deviation `sqrt(rate / (1 - rate))`.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as input.

    References:
        - [Dropout: A Simple Way to Prevent Neural Networks from Overfitting
          Srivastava, Hinton, et al.
          2014](http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)

    Polyaxonfile usage:

    ```yaml
    GaussianDropout:
      rate: 0.7
    ```
    """
    IDENTIFIER = 'GaussianDropout'
    SCHEMA = GaussianDropoutSchema

    def __init__(self, rate, **kwargs):
        super(GaussianDropoutConfig, self).__init__(**kwargs)
        self.rate = rate


class AlphaDropoutSchema(BaseLayerSchema):
    rate = fields.Float(validate=validate.Range(0, 1))
    noise_shape = fields.List(fields.Int(), default=None, missing=None)
    seed = fields.Int(default=None, missing=None)

    @staticmethod
    def schema_config():
        return AlphaDropoutConfig


class AlphaDropoutConfig(BaseLayerConfig):
    """Applies Alpha Dropout to the input.

    Alpha Dropout is a `Dropout` that keeps mean and variance of inputs
    to their original values, in order to ensure the self-normalizing property
    even after this dropout.
    Alpha Dropout fits well to Scaled Exponential Linear Units
    by randomly setting activations to the negative saturation value.

    Args:
        rate: float, drop probability (as with `Dropout`).
            The multiplicative noise will have
            standard deviation `sqrt(rate / (1 - rate))`.
        seed: A Python integer to use as random seed.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as input.

    References:
        - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)

    Polyaxonfile usage:

    ```yaml
    AlphaDropout:
      rate: 0.7
    ```
    """
    IDENTIFIER = 'AlphaDropout'
    SCHEMA = AlphaDropoutSchema

    def __init__(self, rate, noise_shape=None, seed=None, **kwargs):
        super(AlphaDropoutConfig, self).__init__(**kwargs)
        self.rate = rate
        self.noise_shape = noise_shape
        self.seed = seed
