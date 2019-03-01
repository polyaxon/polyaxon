# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema


class WrapperSchema(BaseLayerSchema):
    layer = fields.Nested('LayerSchema')

    @staticmethod
    def schema_config():
        return WrapperConfig


class WrapperConfig(BaseLayerConfig):
    """Abstract wrapper base class.

    Wrappers take another layer and augment it in various ways.
    Do not use this class as a layer, it is only an abstract base class.
    Two usable wrappers are the `TimeDistributed` and `Bidirectional` wrappers.

    Args:
        layer: The layer to be wrapped.
    """
    IDENTIFIER = 'Wrapper'
    SCHEMA = WrapperSchema

    def __init__(self, layer, **kwargs):
        super(WrapperConfig, self).__init__(**kwargs)
        self.layer = layer


class TimeDistributedSchema(WrapperSchema):
    @staticmethod
    def schema_config():
        return TimeDistributedConfig


class TimeDistributedConfig(WrapperConfig):
    """This wrapper allows to apply a layer to every temporal slice of an input.

    The input should be at least 3D, and the dimension of index one
    will be considered to be the temporal dimension.

    Consider a batch of 32 samples,
    where each sample is a sequence of 10 vectors of 16 dimensions.
    The batch input shape of the layer is then `(32, 10, 16)`,
    and the `input_shape`, not including the samples dimension, is `(10, 16)`.

    You can then use `TimeDistributed` to apply a `Dense` layer
    to each of the 10 timesteps, independently:

    ```python
    # as the first layer in a model
    x = TimeDistributed(Dense(8))(x)
    # now x.output_shape == (None, 10, 8)
    ```

    The output will then have shape `(32, 10, 8)`.

    In subsequent layers, there is no need for the `input_shape`:

    ```python
    x = TimeDistributed(Dense(32))(x)
    # now x.output_shape == (None, 10, 32)
    ```

    The output will then have shape `(32, 10, 32)`.

    `TimeDistributed` can be used with arbitrary layers, not just `Dense`,
    for instance with a `Conv2D` layer:

    ```python
    x = TimeDistributed(Conv2D(64, (3, 3)))(x)
    ```

    Args:
        layer: a layer instance.

    Polyaxonfile usage:

    ```yaml
    TimeDistributed:
      layer:
        Dense:
          units: 2
    ```
    """
    IDENTIFIER = 'TimeDistributed'
    SCHEMA = TimeDistributedSchema


class BidirectionalSchema(WrapperSchema):

    @staticmethod
    def schema_config():
        return BidirectionalConfig


class BidirectionalConfig(WrapperConfig):
    """Bidirectional wrapper for RNNs.

    Args:
        layer: `Recurrent` instance.
        merge_mode: Mode by which outputs of the
            forward and backward RNNs will be combined.
            One of {'sum', 'mul', 'concat', 'ave', None}.
            If None, the outputs will not be combined,
            they will be returned as a list.

    Raises:
        ValueError: In case of invalid `merge_mode` argument.

    Example:

    ```python
    x = Bidirectional(plx.layers.LSTM(units=128, dropout=0.2, recurrent_dropout=0.2))(x)
    ```

    Polyaxonfile usage:

    ```yaml
    Bidirectional:
      layer:
        LSTM:
          units: 128
          dropout: 0.2
          recurrent_dropout: 0.2
    ```
    """
    IDENTIFIER = 'Bidirectional'
    SCHEMA = BidirectionalSchema
