# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_dump, post_load

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import InitializerSchema, UniformInitializerConfig
from polyaxon_schemas.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.regularizations import RegularizerSchema


class EmbeddingSchema(BaseLayerSchema):
    input_dim = fields.Int()
    output_dim = fields.Int()
    embeddings_initializer = fields.Nested(InitializerSchema, allow_none=True)
    embeddings_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    embeddings_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    mask_zero = fields.Bool(default=False, missing=False)
    input_length = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EmbeddingConfig(**data)

    @post_dump
    def unmake(self, data):
        return EmbeddingConfig.remove_reduced_attrs(data)


class EmbeddingConfig(BaseLayerConfig):
    """Turns positive integers (indexes) into dense vectors of fixed size.

    eg. [[4], [20]] -> [[0.25, 0.1], [0.6, -0.2]]

    This layer can only be used as the first layer in a model.

    Args:
        input_dim: int > 0. Size of the vocabulary,
            i.e. maximum integer index + 1.
        output_dim: int >= 0. Dimension of the dense embedding.
        embeddings_initializer: Initializer for the `embeddings` matrix.
        embeddings_regularizer: Regularizer function applied to
              the `embeddings` matrix.
        embeddings_constraint: Constraint function applied to
              the `embeddings` matrix.
        mask_zero: Whether or not the input value 0 is a special "padding"
            value that should be masked out.
            This is useful when using recurrent layers,
            which may take variable length inputs.
            If this is `True` then all subsequent layers
            in the model need to support masking or an exception will be raised.
            If mask_zero is set to True, as a consequence, index 0 cannot be
            used in the vocabulary (input_dim should equal size of
            vocabulary + 1).
        input_length: Length of input sequences, when it is constant.
            This argument is required if you are going to connect
            `Flatten` then `Dense` layers upstream
            (without it, the shape of the dense outputs cannot be computed).

    Input shape:
        2D tensor with shape: `(batch_size, sequence_length)`.

    Output shape:
        3D tensor with shape: `(batch_size, sequence_length, output_dim)`.

    References:
        - [A Theoretically Grounded Application of Dropout in Recurrent Neural
          Networks](http://arxiv.org/abs/1512.05287)

    Example:

    ```python
    # input_length=10
    x = Embedding(1000, 64)(x)
    # the model will take as input an integer matrix of size (batch, input_length).
    # the largest integer (i.e. word index) in the input should be no larger
    than 999 (vocabulary size).
    # now x.output_shape == (None, 10, 64), where None is the batch
    dimension.
    ```

    Polyaxonfile usage:

    ```yaml
    Embedding:
      input_dim: 1000
      output_dim: 32
    ```
    """
    IDENTIFIER = 'Embedding'
    SCHEMA = EmbeddingSchema

    def __init__(self,
                 input_dim,
                 output_dim,
                 embeddings_initializer=UniformInitializerConfig(),
                 embeddings_regularizer=None,
                 activity_regularizer=None,
                 embeddings_constraint=None,
                 mask_zero=False,
                 input_length=None,
                 **kwargs):
        super(EmbeddingConfig, self).__init__(**kwargs)
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.embeddings_initializer = embeddings_initializer
        self.embeddings_regularizer = embeddings_regularizer
        self.activity_regularizer = activity_regularizer
        self.embeddings_constraint = embeddings_constraint
        self.mask_zero = mask_zero
        self.input_length = input_length
