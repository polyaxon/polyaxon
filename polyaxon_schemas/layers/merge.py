# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_dump, post_load

from polyaxon_schemas.base import BaseMultiSchema
from polyaxon_schemas.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.utils import ObjectOrListObject


class AddSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AddConfig(**data)

    @post_dump
    def unmake(self, data):
        return AddConfig.remove_reduced_attrs(data)


class AddConfig(BaseLayerConfig):
    """Layer that adds a list of inputs.

    It takes as input a list of tensors,
    all of the same shape, and returns
    a single tensor (also of the same shape).

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Add:
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Add'
    SCHEMA = AddSchema


class SubtractSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SubtractConfig(**data)

    @post_dump
    def unmake(self, data):
        return SubtractConfig.remove_reduced_attrs(data)


class SubtractConfig(BaseLayerConfig):
    """Layer that subtracts two inputs.

    It takes as input a list of tensors of size 2,
    both of the same shape, and returns a single tensor, (inputs[0] - inputs[1]),
    also of the same shape.

    Examples:

    ```python
    # input1.shape == (16,)
    x1 = Dense(8, activation='relu')(input1)
    # input2.shape == (32,)
    x2 = Dense(8, activation='relu')(input2)
    subtracted = Subtract()([x1, x2])
    ```

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Subtract:
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Subtract'
    SCHEMA = SubtractSchema


class MultiplySchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MultiplyConfig(**data)

    @post_dump
    def unmake(self, data):
        return MultiplyConfig.remove_reduced_attrs(data)


class MultiplyConfig(BaseLayerConfig):
    """Layer that multiplies (element-wise) a list of inputs.

    It takes as input a list of tensors,
    all of the same shape, and returns
    a single tensor (also of the same shape).

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Multiply:
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Multiply'
    SCHEMA = MultiplySchema


class AverageSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AverageConfig(**data)

    @post_dump
    def unmake(self, data):
        return AverageConfig.remove_reduced_attrs(data)


class AverageConfig(BaseLayerConfig):
    """Layer that averages a list of inputs.

    It takes as input a list of tensors,
    all of the same shape, and returns
    a single tensor (also of the same shape).

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Average:
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Average'
    SCHEMA = AverageSchema


class MaximumSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MaximumConfig(**data)

    @post_dump
    def unmake(self, data):
        return MaximumConfig.remove_reduced_attrs(data)


class MaximumConfig(BaseLayerConfig):
    """Layer that computes the maximum (element-wise) a list of inputs.

    It takes as input a list of tensors,
    all of the same shape, and returns
    a single tensor (also of the same shape).

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Maximum:
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Maximum'
    SCHEMA = MaximumSchema


class ConcatenateSchema(BaseLayerSchema):
    axis = fields.Int(default=-1, missing=-1)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ConcatenateConfig(**data)

    @post_dump
    def unmake(self, data):
        return ConcatenateConfig.remove_reduced_attrs(data)


class ConcatenateConfig(BaseLayerConfig):
    """Layer that concatenates a list of inputs.

    It takes as input a list of tensors,
    all of the same shape expect for the concatenation axis,
    and returns a single tensor, the concatenation of all inputs.

    Args:
        axis: Axis along which to concatenate.
        **kwargs: standard layer keyword arguments.

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Concatenate:
          axis: 1
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Concatenate'
    SCHEMA = ConcatenateSchema

    def __init__(self, axis=-1, **kwargs):
        super(ConcatenateConfig, self).__init__(**kwargs)
        self.axis = axis


class DotSchema(BaseLayerSchema):
    axes = ObjectOrListObject(fields.Int)
    normalize = fields.Bool(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return DotConfig(**data)

    @post_dump
    def unmake(self, data):
        return DotConfig.remove_reduced_attrs(data)


class DotConfig(BaseLayerConfig):
    """Layer that computes a dot product between samples in two tensors.

    E.g. if applied to two tensors `a` and `b` of shape `(batch_size, n)`,
    the output will be a tensor of shape `(batch_size, 1)`
    where each entry `i` will be the dot product between
    `a[i]` and `b[i]`.

    Args:
        axes: Integer or tuple of integers,
            axis or axes along which to take the dot product.
        normalize: Whether to L2-normalize samples along the
            dot product axis before taking the dot product.
            If set to True, then the output of the dot product
            is the cosine proximity between the two samples.
        **kwargs: Standard layer keyword arguments.

    Polyaxonfile usage:

    ```yaml
    - Dense:
        units: 10
        activation: softmax
        name: dense1

    - Dense:
        units: 10
        activation: softmax
        name: dense2

    - Merge:
        Dot:
          axes: [1, 2]
          inbound_nodes: [dense1, dense2]
    ```
    """
    IDENTIFIER = 'Dot'
    SCHEMA = DotSchema

    def __init__(self, axes, normalize=False, **kwargs):
        super(DotConfig, self).__init__(**kwargs)
        self.axes = axes
        self.normalize = normalize


class MergeSchema(BaseMultiSchema):
    __multi_schema_name__ = 'Merge'
    __configs__ = {
        AddConfig.IDENTIFIER: AddConfig,
        MultiplyConfig.IDENTIFIER: MultiplyConfig,
        AverageConfig.IDENTIFIER: AverageConfig,
        MaximumConfig.IDENTIFIER: MaximumConfig,
        ConcatenateConfig.IDENTIFIER: ConcatenateConfig,
        DotConfig.IDENTIFIER: DotConfig,
    }


class MergeConfig(BaseLayerConfig):
    IDENTIFIER = 'Merge'
    SCHEMA = MergeSchema
