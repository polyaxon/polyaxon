# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.utils import ObjectOrListObject


class BaseBridgeSchema(Schema):
    state_size = ObjectOrListObject(fields.Int, allow_none=True)
    name = fields.Str(allow_none=True)


class BaseBridgeConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self, state_size=None, name=None):
        self.state_size = state_size
        self.name = name


class LatentBridgeSchema(BaseBridgeSchema):
    latent_dim = fields.Int(allow_none=True)
    mean = fields.Float(allow_none=True)
    stddev = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LatentBridgeConfig(**data)

    @post_dump
    def unmake(self, data):
        return LatentBridgeConfig.remove_reduced_attrs(data)


class LatentBridgeConfig(BaseBridgeConfig):
    """A bridge that create a latent space based on the encoder output.

    This bridge could be used by VAE.

    Args(programmatic):
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.

    Args:
        latent_dim: `int`. The latent dimension to use.
        name: `str`. The name of this subgraph, used for creating the scope.

    Attributes:
        z_mean: `Tensor`. The latent distribution mean.
        z_log_sigma: `Tensor`. The latent distribution log variance.

    Returns:
        `BridgeSpec`

    Programmatic usage:

    ```python
    def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
        return plx.bridges.LatentBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)
    ```

    Polyaxonfile usage:

    ```yaml
    model:
      generator:
        ...
        bridge: LatentBridge
        encoder:
          input_layers: image
          layers:
            - Dense:
                units: 128
            - Dense:
                units: 256
                name: encoded
        decoder:
          input_layers: encoded
          layers:
            - Dense:
                units: 256
            - Dense:
                units: 784
    ```
    """
    IDENTIFIER = 'LatentBridge'
    SCHEMA = LatentBridgeSchema

    def __init__(self, latent_dim=1, mean=0., stddev=1., **kwargs):
        super(LatentBridgeConfig, self).__init__(**kwargs)
        self.latent_dim = latent_dim
        self.mean = mean
        self.stddev = stddev


class NoOpBridgeSchema(BaseBridgeSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return NoOpBridgeConfig(**data)

    @post_dump
    def unmake(self, data):
        return NoOpBridgeConfig.remove_reduced_attrs(data)


class NoOpBridgeConfig(BaseBridgeConfig):
    """A bridge that passes the encoder output to the decoder.

    This bridge could be used by VAE.

    Args(programmatic):
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.

    Args:
        state_size: `int`. The latent dimension to use.
        name: `str`. The name of this subgraph, used for creating the scope.

    Returns:
        `BridgeSpec`

    Programmatic usage:

    ```python
    def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
        return plx.bridges.NoOpBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)
    ```

    Polyaxonfile usage:

    ```yaml
    model:
      generator:
        ...
        bridge: NoOpBridge
        encoder:
          input_layers: image
          layers:
            - Dense:
                units: 128
            - Dense:
                units: 256
                name: encoded
        decoder:
          input_layers: encoded
          layers:
            - Dense:
                units: 256
            - Dense:
                units: 784
    ```
    """
    IDENTIFIER = 'NoOpBridge'
    SCHEMA = NoOpBridgeSchema


class BridgeSchema(BaseMultiSchema):
    __multi_schema_name__ = 'bridge'
    __configs__ = {
        LatentBridgeConfig.IDENTIFIER: LatentBridgeConfig,
        NoOpBridgeConfig.IDENTIFIER: NoOpBridgeConfig,
    }
