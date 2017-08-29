# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load, validate

from polyaxon_schemas.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.utils import DType


class ResizeSchema(BaseLayerSchema):
    height = fields.Int()
    width = fields.Int()
    method = fields.Int(allow_none=True, validate=validate.Range(min=0, max=4))
    align_corners = fields.Bool(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ResizeConfig(**data)


class ResizeConfig(BaseLayerConfig):
    SCHEMA = ResizeSchema
    IDENTIFIER = 'Resize'

    def __init__(self, height, width, method=None, align_corners=False, **kwargs):
        super(ResizeConfig, self).__init__(**kwargs)
        self.height = height
        self.width = width
        self.method = method
        self.align_corners = align_corners


class CentralCropSchema(BaseLayerSchema):
    central_fraction = fields.Float(validate=validate.Range(0., 1.))
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return CentralCropConfig(**data)


class CentralCropConfig(BaseLayerConfig):
    SCHEMA = CentralCropSchema
    IDENTIFIER = 'CentralCrop'

    def __init__(self, central_fraction, **kwargs):
        super(CentralCropConfig, self).__init__(**kwargs)
        self.central_fraction = central_fraction


class RandomCropSchema(BaseLayerSchema):
    height = fields.Int()
    width = fields.Int()
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return RandomCropConfig(**data)


class RandomCropConfig(BaseLayerConfig):
    SCHEMA = RandomCropSchema
    IDENTIFIER = 'RandomCrop'

    def __init__(self, height, width, **kwargs):
        super(RandomCropConfig, self).__init__(**kwargs)
        self.height = height
        self.width = width


class ExtractGlimpseSchema(BaseLayerSchema):
    size = fields.List(fields.Int, validate=validate.Length(equal=2))
    offsets = fields.List(fields.Int, validate=validate.Length(equal=2))
    centered = fields.Bool(allow_none=True)
    normalized = fields.Bool(allow_none=True)
    uniform_noise = fields.Bool(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ExtractGlimpseConfig(**data)


class ExtractGlimpseConfig(BaseLayerConfig):
    SCHEMA = ExtractGlimpseSchema
    IDENTIFIER = 'ExtractGlimpse'

    def __init__(self,
                 size,
                 offsets,
                 centered=None,
                 normalized=None,
                 uniform_noise=None,
                 **kwargs):
        super(ExtractGlimpseConfig, self).__init__(**kwargs)
        self.size = size
        self.offsets = offsets
        self.centered = centered
        self.normalized = normalized
        self.uniform_noise = uniform_noise


class ToBoundingBoxSchema(BaseLayerSchema):
    offset_height = fields.Int(validate=lambda n: n >= 0)
    offset_width = fields.Int(validate=lambda n: n >= 0)
    target_height = fields.Int(validate=lambda n: n >= 0)
    target_width = fields.Int(validate=lambda n: n >= 0)
    method = fields.Str(allow_none=True, validate=validate.OneOf(['crop', 'pad']))
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ToBoundingBoxConfig(**data)


class ToBoundingBoxConfig(BaseLayerConfig):
    SCHEMA = ToBoundingBoxSchema
    IDENTIFIER = 'ToBoundingBox'

    def __init__(self,
                 offset_height,
                 offset_width,
                 target_height,
                 target_width,
                 method='crop',
                 **kwargs):
        super(ToBoundingBoxConfig, self).__init__(**kwargs)
        self.offset_height = offset_height
        self.offset_width = offset_width
        self.target_height = target_height
        self.target_width = target_width
        self.method = method


class FlipSchema(BaseLayerSchema):
    axis = fields.Int(allow_none=True, validate=lambda n: n >= 0)
    is_random = fields.Bool(allow_none=True)
    seed = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return FlipConfig(**data)


class FlipConfig(BaseLayerConfig):
    SCHEMA = FlipSchema
    IDENTIFIER = 'Flip'

    def __init__(self, axis=0, is_random=False, seed=None, **kwargs):
        super(FlipConfig, self).__init__(**kwargs)
        self.axis = axis
        self.is_random = is_random
        self.seed = seed


class TransposeSchema(BaseLayerSchema):
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TransposeConfig(**data)


class TransposeConfig(BaseLayerConfig):
    SCHEMA = TransposeSchema
    IDENTIFIER = 'Transpose'


class Rotate90Schema(BaseLayerSchema):
    k = fields.Int(allow_none=True)
    is_random = fields.Bool(allow_none=True)
    seed = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return Rotate90Config(**data)


class Rotate90Config(BaseLayerConfig):
    SCHEMA = Rotate90Schema
    IDENTIFIER = 'Rotate90'

    def __init__(self, k=1, is_random=False, seed=None, **kwargs):
        super(Rotate90Config, self).__init__(**kwargs)
        self.k = k
        self.is_random = is_random
        self.seed = seed


class ConvertColorSpaceSchema(BaseLayerSchema):
    from_space = fields.Str(validate=validate.OneOf(['rgb', 'grayscale', 'hsv']))
    to_space = fields.Str(validate=validate.OneOf(['rgb', 'grayscale', 'hsv']))
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ConvertColorSpaceConfig(**data)


class ConvertColorSpaceConfig(BaseLayerConfig):
    SCHEMA = ConvertColorSpaceSchema
    IDENTIFIER = 'ConvertColorSpace'

    def __init__(self, from_space, to_space, **kwargs):
        super(ConvertColorSpaceConfig, self).__init__(**kwargs)
        self.from_space = from_space
        self.to_space = to_space


class ConvertImagesDtypeSchema(BaseLayerSchema):
    dtype = DType()
    saturate = fields.Bool(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ConvertImagesDtypeConfig(**data)


class ConvertImagesDtypeConfig(BaseLayerConfig):
    SCHEMA = ConvertImagesDtypeSchema
    IDENTIFIER = 'ConvertImagesDtype'

    def __init__(self, dtype, saturate=False, **kwargs):
        super(ConvertImagesDtypeConfig, self).__init__(**kwargs)
        self.dtype = dtype
        self.saturate = saturate


class AdjustBrightnessSchema(BaseLayerSchema):
    delta = fields.Float()
    is_random = fields.Bool(allow_none=True)
    seed = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AdjustBrightnessConfig(**data)


class AdjustBrightnessConfig(BaseLayerConfig):
    SCHEMA = AdjustBrightnessSchema
    IDENTIFIER = 'AdjustBrightness'

    def __init__(self, delta, is_random=False, seed=None, **kwargs):
        super(AdjustBrightnessConfig, self).__init__(**kwargs)
        self.delta = delta
        self.is_random = is_random
        self.seed = seed


class AdjustContrastSchema(BaseLayerSchema):
    contrast_factor = fields.Float()
    contrast_factor_max = fields.Float(allow_none=True)
    is_random = fields.Bool(allow_none=True)
    seed = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AdjustContrastConfig(**data)


class AdjustContrastConfig(BaseLayerConfig):
    SCHEMA = AdjustContrastSchema
    IDENTIFIER = 'AdjustContrast'

    def __init__(self,
                 contrast_factor,
                 contrast_factor_max=None,
                 is_random=False,
                 seed=None,
                 **kwargs):
        super(AdjustContrastConfig, self).__init__(**kwargs)
        self.contrast_factor = contrast_factor
        self.contrast_factor_max = contrast_factor_max
        self.is_random = is_random
        self.seed = seed


class AdjustHueSchema(BaseLayerSchema):
    delta = fields.Float(validate=validate.Range(min=-1., max=1.))
    is_random = fields.Bool(allow_none=True)
    seed = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AdjustHueConfig(**data)


class AdjustHueConfig(BaseLayerConfig):
    SCHEMA = AdjustHueSchema
    IDENTIFIER = 'AdjustHue'

    def __init__(self, delta, is_random=False, seed=None, **kwargs):
        super(AdjustHueConfig, self).__init__(**kwargs)
        self.delta = delta
        self.is_random = is_random
        self.seed = seed


class AdjustSaturationSchema(BaseLayerSchema):
    saturation_factor = fields.Float()
    saturation_factor_max = fields.Float(allow_none=True)
    is_random = fields.Bool(allow_none=True)
    seed = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AdjustSaturationConfig(**data)


class AdjustSaturationConfig(BaseLayerConfig):
    SCHEMA = AdjustSaturationSchema
    IDENTIFIER = 'AdjustSaturation'

    def __init__(self, saturation_factor, saturation_factor_max=None, is_random=False,
                 seed=None, **kwargs):
        super(AdjustSaturationConfig, self).__init__(**kwargs)
        self.saturation_factor = saturation_factor
        self.saturation_factor_max = saturation_factor_max
        self.is_random = is_random
        self.seed = seed


class AdjustGammaSchema(BaseLayerSchema):
    gamma = fields.Float(validate=lambda n: n > 0.)
    gain = fields.Float(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AdjustGammaConfig(**data)


class AdjustGammaConfig(BaseLayerConfig):
    SCHEMA = AdjustGammaSchema
    IDENTIFIER = 'AdjustGamma'

    def __init__(self, gamma=1, gain=1, **kwargs):
        super(AdjustGammaConfig, self).__init__(**kwargs)
        self.gamma = gamma
        self.gain = gain


class StandardizationSchema(BaseLayerSchema):
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return StandardizationConfig(**data)


class StandardizationConfig(BaseLayerConfig):
    SCHEMA = StandardizationSchema
    IDENTIFIER = 'Standardization'


class DrawBoundingBoxesSchema(BaseLayerSchema):
    boxes = fields.List(fields.Float, validate=validate.Length(equal=3))
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return DrawBoundingBoxesConfig(**data)


class DrawBoundingBoxesConfig(BaseLayerConfig):
    SCHEMA = DrawBoundingBoxesSchema
    IDENTIFIER = 'DrawBoundingBoxes'

    def __init__(self, boxes, **kwargs):
        super(DrawBoundingBoxesConfig, self).__init__(**kwargs)
        self.boxes = boxes


class TotalVariationSchema(BaseLayerSchema):
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TotalVariationConfig(**data)


class TotalVariationConfig(BaseLayerConfig):
    SCHEMA = TotalVariationSchema
    IDENTIFIER = 'TotalVariation'
