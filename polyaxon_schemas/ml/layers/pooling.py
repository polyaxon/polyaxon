# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.fields import ObjectOrListObject
from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema


class MaxPooling1DSchema(BaseLayerSchema):
    pool_size = fields.Int(default=2, missing=2, allow_none=True)
    strides = fields.Int(default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))

    @staticmethod
    def schema_config():
        return MaxPooling1DConfig


class MaxPooling1DConfig(BaseLayerConfig):
    """Max pooling operation for temporal data.

    Args:
        pool_size: Integer, size of the max pooling windows.
        strides: Integer, or None. Factor by which to downscale.
            E.g. 2 will halve the input.
            If None, it will default to `pool_size`.
        padding: One of `"valid"` or `"same"` (case-insensitive).

    Input shape:
        3D tensor with shape: `(batch_size, steps, features)`.

    Output shape:
        3D tensor with shape: `(batch_size, downsampled_steps, features)`.

    Polyaxonfile usage:

    ```yaml
    MaxPooling1D:
      pool_size: 2
    ```
    """
    IDENTIFIER = 'MaxPooling1D'
    SCHEMA = MaxPooling1DSchema

    def __init__(self, pool_size=2, strides=None, padding='valid', **kwargs):
        super(MaxPooling1DConfig, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding


class AveragePooling1DSchema(BaseLayerSchema):
    pool_size = fields.Int(default=2, missing=2, allow_none=True)
    strides = fields.Int(default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))

    @staticmethod
    def schema_config():
        return AveragePooling1DConfig


class AveragePooling1DConfig(BaseLayerConfig):
    """Average pooling for temporal data.

    Args:
        pool_size: Integer, size of the max pooling windows.
        strides: Integer, or None. Factor by which to downscale.
            E.g. 2 will halve the input.
            If None, it will default to `pool_size`.
        padding: One of `"valid"` or `"same"` (case-insensitive).

    Input shape:
        3D tensor with shape: `(batch_size, steps, features)`.

    Output shape:
        3D tensor with shape: `(batch_size, downsampled_steps, features)`.

    Polyaxonfile usage:

    ```yaml
    AveragePooling1D:
      pool_size: 2
    ```
    """
    IDENTIFIER = 'AveragePooling1D'
    SCHEMA = AveragePooling1DSchema

    def __init__(self, pool_size=2, strides=None, padding='valid', **kwargs):
        super(AveragePooling1DConfig, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding


class MaxPooling2DSchema(BaseLayerSchema):
    pool_size = ObjectOrListObject(fields.Int, min=2, max=2, default=(2, 2), missing=(2, 2))
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return MaxPooling2DConfig


class MaxPooling2DConfig(BaseLayerConfig):
    """Max pooling operation for spatial data.

    Args:
        pool_size: integer or tuple of 2 integers,
            factors by which to downscale (vertical, horizontal).
            (2, 2) will halve the input in both spatial dimension.
            If only one integer is specified, the same window length
            will be used for both dimensions.
        strides: Integer, tuple of 2 integers, or None.
            Strides values.
            If None, it will default to `pool_size`.
        padding: One of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            4D tensor with shape:
            `(batch_size, rows, cols, channels)`
        - If `data_format='channels_first'`:
            4D tensor with shape:
            `(batch_size, channels, rows, cols)`

    Output shape:
        - If `data_format='channels_last'`:
            4D tensor with shape:
            `(batch_size, pooled_rows, pooled_cols, channels)`
        - If `data_format='channels_first'`:
            4D tensor with shape:
            `(batch_size, channels, pooled_rows, pooled_cols)`

    Polyaxonfile usage:

    ```yaml
    MaxPooling2D:
      pool_size: [2, 2]
    ```
    """
    IDENTIFIER = 'MaxPooling2D'
    SCHEMA = MaxPooling2DSchema

    def __init__(self, pool_size=(2, 2), strides=None, padding='valid', data_format=None, **kwargs):
        super(MaxPooling2DConfig, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format


class AveragePooling2DSchema(BaseLayerSchema):
    pool_size = ObjectOrListObject(fields.Int, min=2, max=2, default=(2, 2), missing=(2, 2))
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return AveragePooling2DConfig


class AveragePooling2DConfig(BaseLayerConfig):
    """Average pooling operation for spatial data.

    Args:
        pool_size: integer or tuple of 2 integers,
            factors by which to downscale (vertical, horizontal).
            (2, 2) will halve the input in both spatial dimension.
            If only one integer is specified, the same window length
            will be used for both dimensions.
        strides: Integer, tuple of 2 integers, or None.
            Strides values.
            If None, it will default to `pool_size`.
        padding: One of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            4D tensor with shape:
            `(batch_size, rows, cols, channels)`
        - If `data_format='channels_first'`:
            4D tensor with shape:
            `(batch_size, channels, rows, cols)`

    Output shape:
        - If `data_format='channels_last'`:
            4D tensor with shape:
            `(batch_size, pooled_rows, pooled_cols, channels)`
        - If `data_format='channels_first'`:
            4D tensor with shape:
            `(batch_size, channels, pooled_rows, pooled_cols)`

    Polyaxonfile usage:

    ```yaml
    AveragePooling2D:
      pool_size: [2, 2]
    ```
    """
    IDENTIFIER = 'AveragePooling2D'
    SCHEMA = AveragePooling2DSchema

    def __init__(self, pool_size=(2, 2), strides=None, padding='valid', data_format=None, **kwargs):
        super(AveragePooling2DConfig, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format


class MaxPooling3DSchema(BaseLayerSchema):
    pool_size = ObjectOrListObject(fields.Int, min=3, max=3, default=(2, 2, 2), missing=(2, 2, 2))
    strides = ObjectOrListObject(fields.Int, min=3, max=3, default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return MaxPooling3DConfig


class MaxPooling3DConfig(BaseLayerConfig):
    """Max pooling operation for 3D data (spatial or spatio-temporal).

    Args:
        pool_size: tuple of 3 integers,
            factors by which to downscale (dim1, dim2, dim3).
            (2, 2, 2) will halve the size of the 3D input in each dimension.
        strides: tuple of 3 integers, or None. Strides values.
        padding: One of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            5D tensor with shape:
            `(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
        - If `data_format='channels_first'`:
            5D tensor with shape:
            `(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

    Output shape:
        - If `data_format='channels_last'`:
            5D tensor with shape:
            `(batch_size, pooled_dim1, pooled_dim2, pooled_dim3, channels)`
        - If `data_format='channels_first'`:
            5D tensor with shape:
            `(batch_size, channels, pooled_dim1, pooled_dim2, pooled_dim3)`

    Polyaxonfile usage:

    ```yaml
    MaxPooling3D:
      pool_size: [2, 2, 2]
    ```
    """
    IDENTIFIER = 'MaxPooling3D'
    SCHEMA = MaxPooling3DSchema

    def __init__(self, pool_size=(2, 2, 2), strides=None, padding='valid', data_format=None,
                 **kwargs):
        super(MaxPooling3DConfig, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format


class AveragePooling3DSchema(BaseLayerSchema):
    pool_size = ObjectOrListObject(fields.Int, min=3, max=3, default=(2, 2, 2), missing=(2, 2, 2))
    strides = ObjectOrListObject(fields.Int, min=3, max=3, default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return AveragePooling3DConfig


class AveragePooling3DConfig(BaseLayerConfig):
    """Average pooling operation for 3D data (spatial or spatio-temporal).

    Args:
        pool_size: tuple of 3 integers,
            factors by which to downscale (dim1, dim2, dim3).
            (2, 2, 2) will halve the size of the 3D input in each dimension.
        strides: tuple of 3 integers, or None. Strides values.
        padding: One of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            5D tensor with shape:
            `(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
        - If `data_format='channels_first'`:
            5D tensor with shape:
            `(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

    Output shape:
        - If `data_format='channels_last'`:
            5D tensor with shape:
            `(batch_size, pooled_dim1, pooled_dim2, pooled_dim3, channels)`
        - If `data_format='channels_first'`:
            5D tensor with shape:
            `(batch_size, channels, pooled_dim1, pooled_dim2, pooled_dim3)`

    Polyaxonfile usage:

    ```yaml
    AveragePooling3D:
      pool_size: [2, 2, 2]
    ```
    """
    IDENTIFIER = 'AveragePooling3D'
    SCHEMA = AveragePooling3DSchema

    def __init__(self, pool_size=(2, 2, 2), strides=None, padding='valid', data_format=None,
                 **kwargs):
        super(AveragePooling3DConfig, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format


class GlobalAveragePooling1DSchema(BaseLayerSchema):
    @staticmethod
    def schema_config():
        return GlobalAveragePooling1DConfig


class GlobalAveragePooling1DConfig(BaseLayerConfig):
    """Global average pooling operation for temporal data.

    Input shape:
        3D tensor with shape: `(batch_size, steps, features)`.

    Output shape:
        2D tensor with shape:
        `(batch_size, channels)`

    Polyaxonfile usage:

    ```yaml
    GlobalAveragePooling1D:
    ```
    """
    IDENTIFIER = 'GlobalAveragePooling1D'
    SCHEMA = GlobalAveragePooling1DSchema


class GlobalMaxPooling1DSchema(BaseLayerSchema):
    @staticmethod
    def schema_config():
        return GlobalMaxPooling1DConfig


class GlobalMaxPooling1DConfig(BaseLayerConfig):
    """Global max pooling operation for temporal data.

    Input shape:
        3D tensor with shape: `(batch_size, steps, features)`.

    Output shape:
        2D tensor with shape:
        `(batch_size, channels)`

    Polyaxonfile usage:

    ```yaml
    GlobalMaxPooling1D:
    ```
    """
    IDENTIFIER = 'GlobalMaxPooling1D'
    SCHEMA = GlobalMaxPooling1DSchema


class GlobalAveragePooling2DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return GlobalAveragePooling2DConfig


class GlobalAveragePooling2DConfig(BaseLayerConfig):
    """Global average pooling operation for spatial data.

    Args:
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            4D tensor with shape:
            `(batch_size, rows, cols, channels)`
        - If `data_format='channels_first'`:
            4D tensor with shape:
            `(batch_size, channels, rows, cols)`

    Output shape:
        2D tensor with shape:
        `(batch_size, channels)`

    Polyaxonfile usage:

    ```yaml
    GlobalAveragePooling2D:
    ```
    """
    IDENTIFIER = 'GlobalAveragePooling2D'
    SCHEMA = GlobalAveragePooling2DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalAveragePooling2DConfig, self).__init__(**kwargs)
        self.data_format = data_format


class GlobalMaxPooling2DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return GlobalMaxPooling2DConfig


class GlobalMaxPooling2DConfig(BaseLayerConfig):
    """Global max pooling operation for spatial data.

    Args:
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            4D tensor with shape:
            `(batch_size, rows, cols, channels)`
        - If `data_format='channels_first'`:
            4D tensor with shape:
            `(batch_size, channels, rows, cols)`

    Output shape:
        2D tensor with shape:
        `(batch_size, channels)`

    Polyaxonfile usage:

    ```yaml
    GlobalMaxPooling2D:
    ```
    """
    IDENTIFIER = 'GlobalMaxPooling2D'
    SCHEMA = GlobalMaxPooling2DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalMaxPooling2DConfig, self).__init__(**kwargs)
        self.data_format = data_format


class GlobalAveragePooling3DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return GlobalAveragePooling3DConfig


class GlobalAveragePooling3DConfig(BaseLayerConfig):
    """Global Average pooling operation for 3D data.

    Args:
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            5D tensor with shape:
            `(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
        - If `data_format='channels_first'`:
            5D tensor with shape:
            `(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

    Output shape:
        2D tensor with shape:
        `(batch_size, channels)`

    Polyaxonfile usage:

    ```yaml
    GlobalAveragePooling3D:
    ```
    """
    IDENTIFIER = 'GlobalAveragePooling3D'
    SCHEMA = GlobalAveragePooling3DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalAveragePooling3DConfig, self).__init__(**kwargs)
        self.data_format = data_format


class GlobalMaxPooling3DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return GlobalMaxPooling3DConfig


class GlobalMaxPooling3DConfig(BaseLayerConfig):
    """Global Max pooling operation for 3D data.

    Args:
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        - If `data_format='channels_last'`:
            5D tensor with shape:
            `(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
        - If `data_format='channels_first'`:
            5D tensor with shape:
            `(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

    Output shape:
        2D tensor with shape:
        `(batch_size, channels)`

    Polyaxonfile usage:

    ```yaml
    GlobalMaxPooling3D:
    ```
    """
    IDENTIFIER = 'GlobalMaxPooling3D'
    SCHEMA = GlobalMaxPooling3DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalMaxPooling3DConfig, self).__init__(**kwargs)
        self.data_format = data_format
