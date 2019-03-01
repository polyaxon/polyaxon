# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.ml.constraints import ConstraintSchema
from polyaxon_schemas.ml.initializations import (
    InitializerSchema,
    OnesInitializerConfig,
    ZerosInitializerConfig
)
from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.ml.regularizations import RegularizerSchema


class BatchNormalizationSchema(BaseLayerSchema):
    axis = fields.Int(default=-1, missing=-1)
    momentum = fields.Float(default=0.99, missing=0.99)
    epsilon = fields.Float(default=1e-3, missing=1e-3)
    center = fields.Bool(default=True, missing=True)
    scale = fields.Bool(default=True, missing=True)
    beta_initializer = fields.Nested(InitializerSchema, allow_none=True)
    gamma_initializer = fields.Nested(InitializerSchema, allow_none=True)
    moving_mean_initializer = fields.Nested(InitializerSchema, allow_none=True)
    moving_variance_initializer = fields.Nested(InitializerSchema, allow_none=True)
    beta_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    gamma_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    beta_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    gamma_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return BatchNormalizationConfig


class BatchNormalizationConfig(BaseLayerConfig):
    """Batch normalization layer (Ioffe and Szegedy, 2014).

    Normalize the activations of the previous layer at each batch,
    i.e. applies a transformation that maintains the mean activation
    close to 0 and the activation standard deviation close to 1.

    Args:
        axis: Integer, the axis that should be normalized
            (typically the features axis).
            For instance, after a `Conv2D` layer with
            `data_format="channels_first"`,
            set `axis=1` in `BatchNormalization`.
        momentum: Momentum for the moving average.
        epsilon: Small float added to variance to avoid dividing by zero.
        center: If True, add offset of `beta` to normalized tensor.
            If False, `beta` is ignored.
        scale: If True, multiply by `gamma`.
            If False, `gamma` is not used.
            When the next layer is linear (also e.g. `nn.relu`),
            this can be disabled since the scaling
            will be done by the next layer.
        beta_initializer: Initializer for the beta weight.
        gamma_initializer: Initializer for the gamma weight.
        moving_mean_initializer: Initializer for the moving mean.
        moving_variance_initializer: Initializer for the moving variance.
        beta_regularizer: Optional regularizer for the beta weight.
        gamma_regularizer: Optional regularizer for the gamma weight.
        beta_constraint: Optional constraint for the beta weight.
        gamma_constraint: Optional constraint for the gamma weight.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as input.

    References:
        - [Batch Normalization: Accelerating Deep Network Training by Reducing
          Internal Covariate Shift](https://arxiv.org/abs/1502.03167)

    Polyaxonfile usage:

    ```yaml
    BatchNormalization:
      momentum: 0.7
    ```
    """
    IDENTIFIER = 'BatchNormalization'
    SCHEMA = BatchNormalizationSchema

    def __init__(self,
                 axis=-1,
                 momentum=0.99,
                 epsilon=1e-3,
                 center=True,
                 scale=True,
                 beta_initializer=ZerosInitializerConfig(),
                 gamma_initializer=OnesInitializerConfig(),
                 moving_mean_initializer=ZerosInitializerConfig(),
                 moving_variance_initializer=OnesInitializerConfig(),
                 beta_regularizer=None,
                 gamma_regularizer=None,
                 beta_constraint=None,
                 gamma_constraint=None,
                 **kwargs):
        super(BatchNormalizationConfig, self).__init__(**kwargs)
        self.axis = axis
        self.momentum = momentum
        self.epsilon = epsilon
        self.center = center
        self.scale = scale
        self.beta_initializer = beta_initializer
        self.gamma_initializer = gamma_initializer
        self.moving_mean_initializer = moving_mean_initializer
        self.moving_variance_initializer = moving_variance_initializer
        self.beta_regularizer = beta_regularizer
        self.gamma_regularizer = gamma_regularizer
        self.beta_constraint = beta_constraint
        self.gamma_constraint = gamma_constraint
