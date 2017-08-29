# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate, post_load

from polyaxon_schemas.utils import ObjectOrListObject
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class MaxPooling1DSchema(BaseLayerSchema):
    pool_size = fields.Int(default=2, missing=2, allow_none=True)
    strides = fields.Int(default=None, missing=None)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MaxPooling1DConfig(**data)


class MaxPooling1DConfig(BaseLayerConfig):
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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AveragePooling1DConfig(**data)


class AveragePooling1DConfig(BaseLayerConfig):
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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MaxPooling2DConfig(**data)


class MaxPooling2DConfig(BaseLayerConfig):
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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AveragePooling2DConfig(**data)


class AveragePooling2DConfig(BaseLayerConfig):
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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MaxPooling3DConfig(**data)


class MaxPooling3DConfig(BaseLayerConfig):
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

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AveragePooling3DConfig(**data)


class AveragePooling3DConfig(BaseLayerConfig):
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
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlobalAveragePooling1DConfig(**data)


class GlobalAveragePooling1DConfig(BaseLayerConfig):
    IDENTIFIER = 'GlobalAveragePooling1D'
    SCHEMA = GlobalAveragePooling1DSchema


class GlobalMaxPooling1DSchema(BaseLayerSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlobalMaxPooling1DConfig(**data)


class GlobalMaxPooling1DConfig(BaseLayerConfig):
    IDENTIFIER = 'GlobalMaxPooling1D'
    SCHEMA = GlobalMaxPooling1DSchema


class GlobalAveragePooling2DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlobalAveragePooling2DConfig(**data)


class GlobalAveragePooling2DConfig(BaseLayerConfig):
    IDENTIFIER = 'GlobalAveragePooling2D'
    SCHEMA = GlobalAveragePooling2DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalAveragePooling2DConfig, self).__init__(**kwargs)
        self.data_format = data_format


class GlobalMaxPooling2DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlobalMaxPooling2DConfig(**data)


class GlobalMaxPooling2DConfig(BaseLayerConfig):
    IDENTIFIER = 'GlobalMaxPooling2D'
    SCHEMA = GlobalMaxPooling2DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalMaxPooling2DConfig, self).__init__(**kwargs)
        self.data_format = data_format


class GlobalAveragePooling3DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlobalAveragePooling3DConfig(**data)


class GlobalAveragePooling3DConfig(BaseLayerConfig):
    IDENTIFIER = 'GlobalAveragePooling3D'
    SCHEMA = GlobalAveragePooling3DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalAveragePooling3DConfig, self).__init__(**kwargs)
        self.data_format = data_format


class GlobalMaxPooling3DSchema(BaseLayerSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return GlobalMaxPooling3DConfig(**data)


class GlobalMaxPooling3DConfig(BaseLayerConfig):
    IDENTIFIER = 'GlobalMaxPooling3D'
    SCHEMA = GlobalMaxPooling3DSchema

    def __init__(self, data_format=None, **kwargs):
        super(GlobalMaxPooling3DConfig, self).__init__(**kwargs)
        self.data_format = data_format
