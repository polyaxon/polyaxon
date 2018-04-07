# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_dump, post_load, validate

from polyaxon_schemas.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.utils import DType

# pylint:disable=too-many-lines


class ResizeSchema(BaseLayerSchema):
    height = fields.Int()
    width = fields.Int()
    method = fields.Int(allow_none=True, validate=validate.Range(min=0, max=4))
    align_corners = fields.Bool(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ResizeConfig(**data)

    @post_dump
    def unmake(self, data):
        return ResizeConfig.remove_reduced_attrs(data)


class ResizeConfig(BaseLayerConfig):
    """Resize `images` to `size` using the specified `method`.
    (A mirror to tf.image resize_images and resize_image_with_crop_or_pad)

    - If method is None: Resizes an image to a target width and height by either centrally
    cropping the image or padding it evenly with zeros.
    If `width` or `height` is greater than the specified `target_width` or
    `target_height` respectively, this op centrally crops along that dimension.
    If `width` or `height` is smaller than the specified `target_width` or
    `target_height` respectively, this op centrally pads with 0 along that dimension.

    - If method is not None: the resized images will be distorted if their original aspect
    ratio is not the same as `size`.

    `method` can be one of:

    *   `None` no distortion.
    *   `ResizeMethod.BILINEAR`: [Bilinear interpolation.](https://en.wikipedia.org/wiki/Bilinear_interpolation)  # noqa
    *   `ResizeMethod.NEAREST_NEIGHBOR`: [Nearest neighbor interpolation.](https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation)  # noqa
    *   `ResizeMethod.BICUBIC`: [Bicubic interpolation.](https://en.wikipedia.org/wiki/Bicubic_interpolation)  # noqa
    *   `ResizeMethod.AREA`: Area interpolation.

    Args:
        height: int32 Target height.
        width: int32 Target width.
        method: ResizeMethod.  Defaults to `ResizeMethod.BILINEAR`.
            Possible values: BILINEAR, NEAREST_NEIGHBOR, BICUBIC, AREA
        align_corners: bool. If true, exactly align all 4 corners of the input and output.
            Only used if method is not None. Defaults to `false`.

    Raises:
        ValueError: if the shape of `images` is incompatible with the
            shape arguments to this function.
        ValueError: if `size` has invalid shape or type.
        ValueError: if an unsupported resize method is specified.

    Returns:
        If `images` was 4-D, a 4-D float Tensor of shape
        `[batch, new_height, new_width, channels]`.
        If `images` was 3-D, a 3-D float Tensor of shape
        `[new_height, new_width, channels]`.

    Polyaxonfile usage:

    ```yaml
    - Resize:
        height: 10
        width: 10
        method: 0
    ```
    """
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
    def make(self, data):
        return CentralCropConfig(**data)

    @post_dump
    def unmake(self, data):
        return CentralCropConfig.remove_reduced_attrs(data)


class CentralCropConfig(BaseLayerConfig):
    """Crop the central region of the image.
    (A mirror to tf.image central_crop)

    Remove the outer parts of an image but retain the central region of the image
    along each dimension. If we specify central_fraction = 0.5, this function
    returns the region marked with "X" in the below diagram.

    ```
     --------
    |........|
    |..XXXX..|
    |..XXXX..|
    |........|   where "X" is the central 50% of the image.
     --------
    ```

    Args:
        central_fraction: float (0, 1], fraction of size to crop

    Raises:
        ValueError: if central_crop_fraction is not within (0, 1].

    Returns:
        If `images` was 4-D, a 4-D float Tensor of shape
        `[batch, new_height, new_width, channels]`.
        If `images` was 3-D, a 3-D float Tensor of shape
        `[new_height, new_width, channels]`.

    Polyaxonfile usage:

    ```yaml
    - CentralCrop:
        central_fraction: 0.5
    ```
    """
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
    def make(self, data):
        return RandomCropConfig(**data)

    @post_dump
    def unmake(self, data):
        return RandomCropConfig.remove_reduced_attrs(data)


class RandomCropConfig(BaseLayerConfig):
    """Randomly crops an image/images to a given size.

    Args:
        height: `float`. The height to crop to.
        width: `float`. The width to crop to.

    Returns:
        If `images` was 4-D, a 4-D float Tensor of shape
        `[batch, new_height, new_width, channels]`.
        If `images` was 3-D, a 3-D float Tensor of shape
        `[new_height, new_width, channels]`.

    Polyaxonfile usage:

    ```yaml
    - RandomCrop:
        height: 10
        width: 10
    ```
    """
    SCHEMA = RandomCropSchema
    IDENTIFIER = 'RandomCrop'

    def __init__(self, height, width, **kwargs):
        super(RandomCropConfig, self).__init__(**kwargs)
        self.height = height
        self.width = width


class ExtractGlimpseSchema(BaseLayerSchema):
    size = fields.List(fields.Int(), validate=validate.Length(equal=2))
    offsets = fields.List(fields.Int(), validate=validate.Length(equal=2))
    centered = fields.Bool(allow_none=True)
    normalized = fields.Bool(allow_none=True)
    uniform_noise = fields.Bool(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExtractGlimpseConfig(**data)

    @post_dump
    def unmake(self, data):
        return ExtractGlimpseConfig.remove_reduced_attrs(data)


class ExtractGlimpseConfig(BaseLayerConfig):
    """Extracts a glimpse from the input tensor.
    (A mirror to tf.image extract_glimpse)

    Returns a set of windows called glimpses extracted at location `offsets`
    from the input tensor. If the windows only partially overlaps the inputs,
    the non overlapping areas will be filled with random noise.

    The result is a 4-D tensor of shape `[batch_size, glimpse_height,
    glimpse_width, channels]`. The channels and batch dimensions are the
    same as that of the input tensor. The height and width of the output
    windows are specified in the `size` parameter.

    The argument `normalized` and `centered` controls how the windows are built:

        * If the coordinates are normalized but not centered, 0.0 and 1.0
            correspond to the minimum and maximum of each height and width
            dimension.
        * If the coordinates are both normalized and centered, they range from -1.0 to 1.0.
            The coordinates (-1.0, -1.0) correspond to the upper left corner, the lower right
            corner is located at (1.0, 1.0) and the center is at (0, 0).
        * If the coordinates are not normalized they are interpreted as numbers of pixels.

    Args:
        size: A `Tensor` of type `int32`.
            A 1-D tensor of 2 elements containing the size of the glimpses to extract.
            The glimpse height must be specified first, following by the glimpse width.
        offsets: A `Tensor` of type `float32`.
            A 2-D integer tensor of shape `[batch_size, 2]` containing
            the y, x locations of the center of each window.
        centered: An optional `bool`. Defaults to `True`.
            indicates if the offset coordinates are centered relative to the image,
            in which case the (0, 0) offset is relative to the center of the input images.
            If false, the (0,0) offset corresponds to the upper left corner of the input images.
        normalized: An optional `bool`. Defaults to `True`.
            indicates if the offset coordinates are normalized.
        uniform_noise: An optional `bool`. Defaults to `True`.
            indicates if the noise should be generated using a
            uniform distribution or a Gaussian distribution.
        name: A name for the operation (optional).

    Returns:
        A `Tensor` of type `float32`.
        A tensor representing the glimpses `[batch_size, glimpse_height, glimpse_width, channels]`.
    """
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
    def make(self, data):
        return ToBoundingBoxConfig(**data)

    @post_dump
    def unmake(self, data):
        return ToBoundingBoxConfig.remove_reduced_attrs(data)


class ToBoundingBoxConfig(BaseLayerConfig):
    """Pad/Crop `image` with zeros to the specified `height` and `width`.
    (A mirror to tf.image pad_to_bounding_box and crop_to_bounding_box)

    If method == 'pad':
        Adds `offset_height` rows of zeros on top, `offset_width` columns of
        zeros on the left, and then pads the image on the bottom and right
        with zeros until it has dimensions `target_height`, `target_width`.

        This op does nothing if `offset_*` is zero and the image already has size
        `target_height` by `target_width`.

    If method == 'crop':
        Crops an image to a specified bounding box.

        This op cuts a rectangular part out of `image`. The top-left corner of the
        returned image is at `offset_height, offset_width` in `image`, and its
        lower-right corner is at `offset_height + target_height, offset_width + target_width`.

    Args:
        offset_height:
            * pad: Number of rows of zeros to add on top.
            * crop: Vertical coordinate of the top-left corner of the result the input.
        offset_width:
            * pad: Number of columns of zeros to add on the left.
            * crop: Horizontal coordinate of the top-left corner of the result in the input.
        target_height: Height of output image.
        target_width: Width of output image.
        method: `crop` or `pad`

    Returns:
        If `image` was 4-D, a 4-D float Tensor of shape
        `[batch, target_height, target_width, channels]`
        If `image` was 3-D, a 3-D float Tensor of shape
        `[target_height, target_width, channels]`

    Raises:
        ValueError: If the shape of `image` is incompatible with the `offset_*` or
        `target_*` arguments, or either `offset_height` or `offset_width` is negative.

    Polyaxonfile usage:

    ```yaml
    - ToBoundingBox:
        offset_height: 10
        offset_width: 10
        target_height: 100
        target_width: 100
    ```
    """
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
    def make(self, data):
        return FlipConfig(**data)

    @post_dump
    def unmake(self, data):
        return FlipConfig.remove_reduced_attrs(data)


class FlipConfig(BaseLayerConfig):
    """Flip (randomly) an image/images.
    (A mirror to tf.image flip_left_right, flip_up_down, random_flip_left_right, and
    random_flip_up_down)

     if axis is 0:
        * flip horizontally (left to right)
     if axis is 1:
        * vertically (upside down).

    Outputs the contents of `images` flipped along the given axis.

    Args:
        axis: `int`. 0 for horizontal, 1 for vertical
        is_random: `bool`, If True, flip randomly.
        seed: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.

    Returns:
        If `image` was 4-D, a 4-D float Tensor of shape
        `[batch, target_height, target_width, channels]`
        If `image` was 3-D, a 3-D float Tensor of shape
        `[target_height, target_width, channels]

    Raises:
        ValueError: if the shape of `image` not supported.

    Polyaxonfile usage:

    ```yaml
    - FlipSchema:
        axis: 0
    ```
    """
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
    def make(self, data):
        return TransposeConfig(**data)

    @post_dump
    def unmake(self, data):
        return TransposeConfig.remove_reduced_attrs(data)


class TransposeConfig(BaseLayerConfig):
    """Transpose an image/images by swapping the first and second dimension.
    (A mirror to tf.image transpose_image)

    Returns:
        If `image` was 4-D, a 4-D float Tensor of shape
        `[batch, target_height, target_width, channels]`
        If `image` was 3-D, a 3-D float Tensor of shape
        `[target_height, target_width, channels]

    Raises:
        ValueError: if the shape of `image` not supported.

    Polyaxonfile usage:

    ```yaml
    - Transpose:
    ```
    """
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
    def make(self, data):
        return Rotate90Config(**data)

    @post_dump
    def unmake(self, data):
        return Rotate90Config.remove_reduced_attrs(data)


class Rotate90Config(BaseLayerConfig):
    """Rotate (randomly) images counter-clockwise by 90 degrees.
    (A mirror to tf.image rot90)

    Args:
        k: A scalar integer. The number of times the image is rotated by 90 degrees.
        is_random: `bool`, If True, adjust randomly.
        seed: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.
        name: A name for this operation (optional).

    Returns:
        If `image` was 4-D, a 4-D float Tensor of shape
        `[batch, target_height, target_width, channels]`
        If `image` was 3-D, a 3-D float Tensor of shape
        `[target_height, target_width, channels]

    Raises:
        ValueError: if the shape of `image` not supported.

    Polyaxonfile usage:

    ```yaml
    - Rotate90:
        k: 2
    ```
    """
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
    def make(self, data):
        return ConvertColorSpaceConfig(**data)

    @post_dump
    def unmake(self, data):
        return ConvertColorSpaceConfig.remove_reduced_attrs(data)


class ConvertColorSpaceConfig(BaseLayerConfig):
    """Converts one or more images from RGB to Grayscale.
    (A mirror to tf.image rgb_to_grayscale, rgb_to_hsv, grayscale_to_rgb, and hsv_to_rgb)

    Outputs a tensor of the same `DType` and rank as `images`.

    Possible conversions:
        * rgb_to_grayscale: The size of the last dimension of the output is 1,
            containing the Grayscale value of the pixels.
        * grayscale_to_rgb: The size of the last dimension of the output is 3,
            containing the RGB value of the pixels.
        * hsv_to_rgb: The output is only well defined if the value in `images` are in `[0,1]`.
        * rgb_to_hsv: The output is only well defined if the value in `images` are in `[0,1]`.
            `output[..., 0]` contains hue, `output[..., 1]` contains saturation, and
            `output[..., 2]` contains value. All HSV values are in `[0,1]`. A hue of 0
            corresponds to pure red, hue 1/3 is pure green, and 2/3 is pure blue.
        * grayscale_to_hsv: grayscale_to_rgb then rgb_to_hsv
        * hsv_to_grayscale: hsv_to_rgb then rgb_to_grayscale.

    Args:
        images: 4-D Tensor of shape `[batch, height, width, channels]`
        from_space: The color to convert from.
        to_space: The color space to convert to.
        name: A name for the operation (optional).

    Returns:
        The converted image(s).

    Polyaxonfile usage:

    ```yaml
    - ConvertColorSpace:
        from_space: rgb
        to_space: grayscale
    ```
    """
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
    def make(self, data):
        return ConvertImagesDtypeConfig(**data)

    @post_dump
    def unmake(self, data):
        return ConvertImagesDtypeConfig.remove_reduced_attrs(data)


class ConvertImagesDtypeConfig(BaseLayerConfig):
    """Convert image(s) to `dtype`, scaling its values if needed.
    (A mirror to tf.image convert_image_dtype)

    Images that are represented using floating point values are expected to have
    values in the range [0,1). Image data stored in integer data types are
    expected to have values in the range `[0,MAX]`, where `MAX` is the largest
    positive representable number for the data type.

    This op converts between data types, scaling the values appropriately before
    casting.

    Note that converting from floating point inputs to integer types may lead to
    over/underflow problems. Set saturate to `True` to avoid such problem in
    problematic conversions. If enabled, saturation will clip the output into the
    allowed range before performing a potentially dangerous cast (and only before
    performing such a cast, i.e., when casting from a floating point to an integer
    type, and when casting from a signed to an unsigned type; `saturate` has no
    effect on casts between floats, or on casts that increase the type's range).

    Args:
        dtype: A `DType` to convert `image` to.
        saturate: If `True`, clip the input before casting (if necessary).
        name: A name for this operation (optional).

    Returns:
        `image`, converted to `dtype`.

    Polyaxonfile usage:

    ```yaml
    - ConvertImagesDtype:
        dtype: float32
    ```
    """
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
    def make(self, data):
        return AdjustBrightnessConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdjustBrightnessConfig.remove_reduced_attrs(data)


class AdjustBrightnessConfig(BaseLayerConfig):
    """Adjust (randomly) the brightness of RGB or Grayscale images.
    (A mirror to tf.image adjust_brightness, random_birightness)

    This is a convenience method that converts an RGB image to float
    representation, adjusts its brightness, and then converts it back to the
    original data type. If several adjustments are chained it is advisable to
    minimize the number of redundant conversions.

    The value `delta` is added to all components of the tensor `image`. Both
    `image` and `delta` are converted to `float` before adding (and `image` is
    scaled appropriately if it is in fixed-point representation). For regular
    images, `delta` should be in the range `[0,1)`, as it is added to the image in
    floating point representation, where pixel values are in the `[0,1)` range.

    If `is_random` is `True`, adjust brightness using a value randomly picked in the
    interval `[-delta, delta)`.

    Args:
        images: A tensor.
        delta: `float`. Amount to add to the pixel values.
        is_random: `bool`, If True, adjust randomly.
        seed: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.

    Returns:
        A brightness-adjusted tensor of the same shape and type as `images`.

    Polyaxonfile usage:

    ```yaml
    - AdjustBrightness:
        delta: 0.5
        is_random: true
    ```
    """
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
    def make(self, data):
        return AdjustContrastConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdjustContrastConfig.remove_reduced_attrs(data)


class AdjustContrastConfig(BaseLayerConfig):
    """Adjust (randomly) the contrast of RGB or grayscale images by contrast factor.
    (A mirror to tf.image adjust_contrast, random_contrast)

    This is a convenience method that converts an RGB image to float
    representation, adjusts its contrast, and then converts it back to the
    original data type. If several adjustments are chained it is advisable to
    minimize the number of redundant conversions.

    `images` is a tensor of at least 3 dimensions.  The last 3 dimensions are
    interpreted as `[height, width, channels]`.  The other dimensions only
    represent a collection of images, such as `[batch, height, width, channels].`

    Contrast is adjusted independently for each channel of each image.

    For each channel, this Op computes the mean of the image pixels in the
    channel and then adjusts each component `x` of each pixel to
    `(x - mean) * contrast_factor + mean`.

    If `is_random` is `True`: Equivalent to `adjust_contrast()` but the value is
        randomly picked in the interval `[contrast_factor, contrast_factor_max]`.

    Args:
        contrast_factor: `float`.  Lower bound for the random contrast factor.
        contrast_factor_max: `float`.  Upper bound for the random contrast factor.
            Used for random adjustment.
        is_random: `bool`, If True, adjust randomly.
        seed: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.

    Returns:
        The contrast-adjusted tensor.

    Raises:
        ValueError: if `contrast_factor_max <= contrast_factor`
                    if `contrast_factor < 0`
                    if `contrast_factor_max` is None (for random.)

    Polyaxonfile usage:

    ```yaml
    - AdjustContrast:
        contrast_factor: 0.5
        is_random: true
    ```
    """
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
    def make(self, data):
        return AdjustHueConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdjustHueConfig.remove_reduced_attrs(data)


class AdjustHueConfig(BaseLayerConfig):
    """Adjust (randomly) hue of an RGB images.
    (A mirror to tf.image adjust_hue, random_hue)

    This is a convenience method that converts an RGB image to float
    representation, converts it to HSV, add an offset to the hue channel, converts
    back to RGB and then back to the original data type. If several adjustments
    are chained it is advisable to minimize the number of redundant conversions.

    `image` is an RGB image.  The image hue is adjusted by converting the
    image to HSV and rotating the hue channel (H) by `delta`.
    The image is then converted back to RGB.

    `delta` must be in the interval `[-1, 1]`.

    If `is_random` is `True` adjust hue but uses a value randomly picked in
    the interval `[-delta, delta]`.

    Args:
        delta: float.  How much to add to the hue channel.
        is_random: `bool`, If True, adjust randomly.
        seed: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.
        name: A name for this operation (optional).

    Returns:
        Adjusted image(s), same shape and DType as `image`.

    Polyaxonfile usage:

    ```yaml
    - AdjustHue:
        delta: 0.5
        is_random: true
    ```
    """
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
    def make(self, data):
        return AdjustSaturationConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdjustSaturationConfig.remove_reduced_attrs(data)


class AdjustSaturationConfig(BaseLayerConfig):
    """Adjust (randomly) saturation of RGB images.
    (A mirror to tf.image adjust_saturation, random_saturation)

    This is a convenience method that converts an RGB image to float
    representation, converts it to HSV, add an offset to the saturation channel,
    converts back to RGB and then back to the original data type. If several
    adjustments are chained it is advisable to minimize the number of redundant
    conversions.

    The image saturation is adjusted by converting the images to HSV and
    multiplying the saturation (S) channel by `saturation_factor` and clipping.
    The images is then converted back to RGB.

    If `is_random` is `True` adjust saturation but uses a value randomly picked in
    the interval `[saturation_factor, saturation_factor_max]`.

    Args:
        saturation_factor: float.  Lower bound for the random saturation factor.
        saturation_factor_max: float.  Upper bound for the random saturation factor.
        is_random: `bool`, If True, adjust randomly.
        seed: An operation-specific seed. It will be used in conjunction
          with the graph-level seed to determine the real seeds that will be
          used in this operation. Please see the documentation of
          set_random_seed for its interaction with the graph-level random seed.
        name: A name for this operation (optional).

    Returns:
        Adjusted image(s), same shape and DType as `image`.

    Raises:

        ValueError: if `saturation_factor_max <= saturation_factor`
                    if `saturation_factor < 0`
                    if `saturation_factor_max is None (for random.)`

    Polyaxonfile usage:

    ```yaml
    - AdjustSaturation:
        saturation_factor: 0.5
        saturation_factor_max: 1.
    ```
    """
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
    def make(self, data):
        return AdjustGammaConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdjustGammaConfig.remove_reduced_attrs(data)


class AdjustGammaConfig(BaseLayerConfig):
    """Performs Gamma Correction on the input image.
    Also known as Power Law Transform. This function transforms the
    input image pixelwise according to the equation Out = In**gamma
    after scaling each pixel to the range 0 to 1.
    (A mirror to tf.image adjust_gamma)

    Args:
        gamma : A scalar. Non negative real number.
        gain  : A scalar. The constant multiplier.

    Returns:
        A Tensor. Gamma corrected output image.

    Notes:
        For gamma greater than 1, the histogram will shift towards left and
        the output image will be darker than the input image.
        For gamma less than 1, the histogram will shift towards right and
        the output image will be brighter than the input image.

    References:
        [1] http://en.wikipedia.org/wiki/Gamma_correction

    Polyaxonfile usage:

    ```yaml
    - AdjustGamma:
        gamma: 1
    ```
    """
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
    def make(self, data):
        return StandardizationConfig(**data)

    @post_dump
    def unmake(self, data):
        return StandardizationConfig.remove_reduced_attrs(data)


class StandardizationConfig(BaseLayerConfig):
    """Linearly scales `image` to have zero mean and unit norm.
    (A mirror to tf.image per_image_standardization)

    This op computes `(x - mean) / adjusted_stddev`, where `mean` is the average
    of all values in image, and
    `adjusted_stddev = max(stddev, 1.0/sqrt(image.NumElements()))`.

    `stddev` is the standard deviation of all values in `image`. It is capped
    away from zero to protect against division by 0 when handling uniform images.

    Returns:
        The standardized image with same shape as `image`.

    Raises:
        ValueError: if the shape of 'image' is incompatible with this function.

    Polyaxonfile usage:

    ```yaml
    - Standardization:
    ```
    """
    SCHEMA = StandardizationSchema
    IDENTIFIER = 'Standardization'


class DrawBoundingBoxesSchema(BaseLayerSchema):
    boxes = fields.List(fields.Float(), validate=validate.Length(equal=3))
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return DrawBoundingBoxesConfig(**data)

    @post_dump
    def unmake(self, data):
        return DrawBoundingBoxesConfig.remove_reduced_attrs(data)


class DrawBoundingBoxesConfig(BaseLayerConfig):
    """Draw bounding boxes on a batch of images.
    (A mirror to tf.image draw_bounding_boxes)

    Outputs a copy of `images` but draws on top of the pixels zero or more bounding
    boxes specified by the locations in `boxes`. The coordinates of the each
    bounding box in `boxes` are encoded as `[y_min, x_min, y_max, x_max]`. The
    bounding box coordinates are floats in `[0.0, 1.0]` relative to the width and
    height of the underlying image.

    For example, if an image is 100 x 200 pixels and the bounding box is
    `[0.1, 0.2, 0.5, 0.9]`, the bottom-left and upper-right coordinates of the
    bounding box will be `(10, 40)` to `(50, 180)`.

    Parts of the bounding box may fall outside the image.

    Args:
        boxes: A `Tensor` of type `float32`.
            3-D with shape `[batch, num_bounding_boxes, 4]` containing bounding boxes.
        name: A name for the operation (optional).

    Returns:
        A `Tensor`. Has the same type as `images`.
        4-D with the same shape as `images`. The batch of input images with
        bounding boxes drawn on the images.

    Polyaxonfile usage:

    ```yaml
    - DrawBoundingBoxes:
        boxes: [0.1, 0.2, 0.5, 0.9]
    ```
    """
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
    def make(self, data):
        return TotalVariationConfig(**data)

    @post_dump
    def unmake(self, data):
        return TotalVariationConfig.remove_reduced_attrs(data)


class TotalVariationConfig(BaseLayerConfig):
    """Calculate and return the total variation for one or more images.

    (A mirror to tf.image total_variation)

    The total variation is the sum of the absolute differences for neighboring
    pixel-values in the input images. This measures how much noise is in the
    images.

    This can be used as a loss-function during optimization so as to suppress
    noise in images. If you have a batch of images, then you should calculate
    the scalar loss-value as the sum:
    `loss = tf.reduce_sum(tf.image.total_variation(images))`

    This implements the anisotropic 2-D version of the formula described here:

    https://en.wikipedia.org/wiki/Total_variation_denoising

    Args:
        name: A name for the operation (optional).

    Raises:
        ValueError: if images.shape is not a 3-D or 4-D vector.

    Returns:
        The total variation of `images`.

        If `images` was 4-D, return a 1-D float Tensor of shape `[batch]` with the
        total variation for each image in the batch.
        If `images` was 3-D, return a scalar float with the total variation for that image.

    Polyaxonfile usage:

    ```yaml
    - TotalVariation:
    ```
    """
    SCHEMA = TotalVariationSchema
    IDENTIFIER = 'TotalVariation'
