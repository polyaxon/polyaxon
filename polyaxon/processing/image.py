# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
# pylint:  disable=too-many-lines

from collections import OrderedDict

import tensorflow as tf

from tensorflow.contrib.keras.python.keras.engine import Layer
from tensorflow.python.ops import random_ops

from polyaxon_schemas.processing.image import (
    ResizeConfig,
    CentralCropConfig,
    RandomCropConfig,
    ExtractGlimpseConfig,
    ToBoundingBoxConfig,
    FlipConfig,
    TransposeConfig,
    Rotate90Config,
    ConvertColorSpaceConfig,
    ConvertImagesDtypeConfig,
    AdjustBrightnessConfig,
    AdjustContrastConfig,
    AdjustHueConfig,
    AdjustSaturationConfig,
    AdjustGammaConfig,
    StandardizationConfig,
    DrawBoundingBoxesConfig,
    TotalVariationConfig,
)

from polyaxon.libs.utils import get_shape, get_name_scope

from polyaxon.libs.base_object import BaseObject


def resize(images, height, width, method=None, align_corners=False):
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
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.
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
    """
    if method is None:
        return tf.image.resize_image_with_crop_or_pad(
            images, target_height=height, target_width=width)

    size = [height, width]
    return tf.image.resize_images(
        images=images, size=size, method=method, align_corners=align_corners)


class Resize(BaseObject, Layer):
    """See `plx.image.resize`'s docstring"""
    CONFIG = ResizeConfig
    __doc__ = ResizeConfig.__doc__

    def __init__(self, height, width, method=None, align_corners=False, **kwargs):
        super(Resize, self).__init__(**kwargs)
        self.height = height
        self.width = width
        self.method = method
        self.alighn_corners = align_corners

    def call(self, inputs, **kwargs):
        return resize(
            images=inputs,
            height=self.height,
            width=self.width,
            method=self.method,
            align_corners=self.alighn_corners)


def central_crop(images, central_fraction):
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
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.
        central_fraction: float (0, 1], fraction of size to crop

    Raises:
        ValueError: if central_crop_fraction is not within (0, 1].

    Returns:
        If `images` was 4-D, a 4-D float Tensor of shape
        `[batch, new_height, new_width, channels]`.
        If `images` was 3-D, a 3-D float Tensor of shape
        `[new_height, new_width, channels]`.
    """
    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        return tf.map_fn(lambda img: tf.image.central_crop(img, central_fraction), images)
    return tf.image.central_crop(images, central_fraction)


class CentralCrop(BaseObject, Layer):
    """See `plx.image.central_crop`'s docstring"""
    CONFIG = CentralCropConfig
    __doc__ = CentralCropConfig.__doc__

    def __init__(self, central_fraction, **kwargs):
        super(CentralCrop, self).__init__(**kwargs)
        self.central_fraction = central_fraction

    def call(self, inputs, **kwargs):
        return central_crop(images=inputs, central_fraction=self.central_fraction)


def random_crop(images, height, width):
    """Randomly crops an image/images to a given size.

    Args:
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.
        height: `float`. The height to crop to.
        width: `float`. The width to crop to.

    Returns:
        If `images` was 4-D, a 4-D float Tensor of shape
        `[batch, new_height, new_width, channels]`.
        If `images` was 3-D, a 3-D float Tensor of shape
        `[new_height, new_width, channels]`.
    """
    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        return tf.map_fn(lambda img: tf.random_crop(img, [height, width, images_shape[-1]]), images)

    return tf.random_crop(images, [height, width, images_shape[-1]])


class RandomCrop(BaseObject, Layer):
    """See `plx.image.random_crop`'s docstring"""
    CONFIG = RandomCropConfig
    __doc__ = RandomCropConfig.__doc__

    def __init__(self, height, width, **kwargs):
        super(RandomCrop, self).__init__(**kwargs)
        self.height = height
        self.width = width

    def call(self, inputs, **kwargs):
        return random_crop(images=inputs, height=self.height, width=self.width)


def extract_glimpse(images, size, offsets, centered=None, normalized=None,
                    uniform_noise=None, name=None):
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
        images: A `Tensor` of type `float32`.
            A 4-D float tensor of shape `[batch_size, height, width, channels]`.
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
    return tf.image.extract_glimpse(
        images, size, offsets, centered, normalized, uniform_noise, name)


class ExtractGlimpse(BaseObject, Layer):
    """See `plx.image.extract_glimpse`'s docstring"""
    CONFIG = ExtractGlimpseConfig
    __doc__ = ExtractGlimpseConfig.__doc__

    def __init__(self, size, offsets, centered=None, normalized=None, uniform_noise=None, **kwargs):
        super(ExtractGlimpse, self).__init__(**kwargs)
        self.size = size
        self.offsets = offsets
        self.centred = centered
        self.normalized = normalized
        self.uniform_noise = uniform_noise

    def call(self, inputs, **kwargs):
        return extract_glimpse(images=inputs,
                               size=self.size,
                               offsets=self.offsets,
                               centered=self.centred,
                               normalized=self.normalized,
                               uniform_noise=self.uniform_noise,
                               name=self.name)


def to_bounding_box(images, offset_height, offset_width, target_height, target_width,
                    method='crop'):
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
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
               3-D Tensor of shape `[height, width, channels]`.
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
    """
    assert method in ['crop', 'pad'], "method should be one of `crop`, `pad`. " \
                                      "received instead `{}`".format(method)

    if method == 'pad':
        return tf.image.pad_to_bounding_box(
            images, offset_height, offset_width, target_height, target_width)

    return tf.image.crop_to_bounding_box(
        images, offset_height, offset_width, target_height, target_width)


class ToBoundingBox(BaseObject, Layer):
    """See `plx.image.to_bounding_box`'s docstring"""
    CONFIG = ToBoundingBoxConfig
    __doc__ = ToBoundingBoxConfig.__doc__

    def __init__(self, offset_height, offset_width, target_height, target_width,
                 method='crop', **kwargs):
        super(ToBoundingBox, self).__init__(**kwargs)
        self.offset_height = offset_height
        self.offset_width = offset_width
        self.target_height = target_height
        self.target_width = target_width
        self.method = method

    def call(self, inputs, **kwargs):
        return to_bounding_box(images=inputs,
                               offset_height=self.offset_height,
                               offset_width=self.offset_width,
                               target_height=self.target_height,
                               target_width=self.target_width,
                               method=self.method)


def flip(images, axis=0, is_random=False, seed=None):
    """Flip (randomly) an image/images.
    (A mirror to tf.image flip_left_right, flip_up_down, random_flip_left_right, and
    random_flip_up_down)

     if axis is 0:
        * flip horizontally (left to right)
     if axis is 1:
        * vertically (upside down).

    Outputs the contents of `images` flipped along the given axis.

    Args:
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.
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
    """
    if axis == 0:
        method = tf.image.flip_left_right if not is_random else tf.image.random_flip_left_right
    elif axis == 1:
        method = tf.image.flip_up_down if not is_random else tf.image.random_flip_up_down
    else:
        raise ValueError("`axis` should be 0 or 1, received `{}`".format(axis))

    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        if is_random:
            return tf.map_fn(lambda img: method(img, seed), images)
        return tf.map_fn(method, images)

    return method(images)


class Flip(BaseObject, Layer):
    """See `plx.image.flip`'s docstring"""
    CONFIG = FlipConfig
    __doc__ = FlipConfig.__doc__

    def __init__(self, axis=0, is_random=False, seed=None, **kwargs):
        super(Flip, self).__init__(**kwargs)
        self.axis = axis
        self.is_random = is_random
        self.seed = seed

    def call(self, inputs, **kwargs):
        return flip(images=inputs, axis=self.axis, is_random=self.is_random, seed=self.seed)


def transpose(images):
    """Transpose an image/images by swapping the first and second dimension.
    (A mirror to tf.image transpose_image)

    Args:
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.

    Returns:
        If `image` was 4-D, a 4-D float Tensor of shape
        `[batch, target_height, target_width, channels]`
        If `image` was 3-D, a 3-D float Tensor of shape
        `[target_height, target_width, channels]

    Raises:
        ValueError: if the shape of `image` not supported.
    """
    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        return tf.map_fn(tf.image.transpose_image, images)

    return tf.image.transpose_image(images)


class Transpose(BaseObject, Layer):
    """See `plx.image.transpose`'s docstring"""
    CONFIG = TransposeConfig
    __doc__ = TransposeConfig.__doc__

    def call(self, inputs, **kwargs):
        return transpose(images=inputs)


def rotate90(images, k=1, is_random=False, seed=None, name=None):
    """Rotate (randomly) images counter-clockwise by 90 degrees.
    (A mirror to tf.image rot90)

    Args:
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.
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
    """
    if is_random:
        k = random_ops.random_shuffle([0, 1, 2, 3], seed=seed)[0]

    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        return tf.map_fn(lambda img: tf.image.rot90(img, k, name), images)

    return tf.image.rot90(images, k, name)


class Rotate90(BaseObject, Layer):
    """See `plx.image.rotate90`'s docstring"""
    CONFIG = Rotate90Config
    __doc__ = Rotate90Config.__doc__

    def __init__(self, k=1, is_random=False, seed=None, **kwargs):
        super(Rotate90, self).__init__(**kwargs)
        self.k = k
        self.is_random = is_random
        self.seed = seed

    def call(self, inputs, **kwargs):
        return rotate90(images=inputs,
                        k=self.k,
                        is_random=self.is_random,
                        seed=self.seed,
                        name=self.name)


def convert_color_space(images, from_space, to_space, name=None):
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
    """
    color_spaces = ('rgb', 'grayscale', 'hsv')
    if from_space not in color_spaces:
        raise ValueError('`from_space` should be one of the values `{}`, '
                         'received instead `{}`'.format(color_spaces, from_space))
    if to_space not in color_spaces:
        raise ValueError('`to_space` should be one of the values `{}`, '
                         'received instead `{}`'.format(color_spaces, to_space))

    if from_space == 'rgb':
        if to_space == 'grayscale':
            return tf.image.rgb_to_grayscale(images=images, name=name)
        if to_space == 'hsv':
            return tf.image.rgb_to_hsv(images=images, name=name)

    if from_space == 'grayscale':
        if to_space == 'rgb':
            return tf.image.grayscale_to_rgb(images=images, name=name)
        if to_space == 'hsv':
            with get_name_scope(name, 'grayscale_to_hsv', [images]):
                _images = tf.image.grayscale_to_rgb(images=images)
                return tf.image.rgb_to_hsv(images=_images)

    if from_space == 'hsv':
        if to_space == 'rgb':
            return tf.image.hsv_to_rgb(images=images, name=name)
        if to_space == 'grayscale':
            with get_name_scope(name, 'hsv_to_grayscale', [images]):
                _images = tf.image.hsv_to_rgb(images=images)
                return tf.image.rgb_to_grayscale(images=_images)


class ConvertColorSpace(BaseObject, Layer):
    """See `plx.image.convert_color_space`'s docstring"""
    CONFIG = ConvertColorSpaceConfig
    __doc__ = ConvertColorSpaceConfig.__doc__

    def __init__(self, from_space, to_space, **kwargs):
        super(ConvertColorSpace, self).__init__(**kwargs)
        self.from_space = from_space
        self.to_space = to_space

    def call(self, inputs, **kwargs):
        return convert_color_space(images=inputs,
                                   from_space=self.from_space,
                                   to_space=self.to_space,
                                   name=self.name)


def convert_images_dtype(images, dtype, saturate=False, name=None):
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
        images: An image.
        dtype: A `DType` to convert `image` to.
        saturate: If `True`, clip the input before casting (if necessary).
        name: A name for this operation (optional).

    Returns:
        `image`, converted to `dtype`.
    """
    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        return tf.map_fn(lambda img: tf.image.convert_image_dtype(
            img, dtype=dtype, saturate=saturate, name=name), images)

    return tf.image.convert_image_dtype(images, dtype=dtype, saturate=saturate, name=name)


class ConvertImagesDtype(BaseObject, Layer):
    """See `plx.image.convert_images_dtype`'s docstring"""
    CONFIG = ConvertImagesDtypeConfig
    __doc__ = ConvertImagesDtypeConfig.__doc__

    def __init__(self, dtype, saturate=False, **kwargs):
        super(ConvertImagesDtype, self).__init__(**kwargs)
        self.dtype = dtype
        self.saturate = saturate

    def call(self, inputs, **kwargs):
        return convert_images_dtype(images=inputs,
                                    dtype=self.dtype,
                                    saturate=self.saturate,
                                    name=self.name)


def adjust_brightness(images, delta, is_random=False, seed=None):
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
    """
    if is_random:
        return tf.image.random_brightness(images, max_delta=delta, seed=seed)
    return tf.image.adjust_brightness(images, delta=delta)


class AdjustBrightness(BaseObject, Layer):
    """See `plx.image.adjust_brightness`'s docstring"""
    CONFIG = AdjustBrightnessConfig
    __doc__ = AdjustBrightnessConfig.__doc__

    def __init__(self, delta, is_random=False, seed=None, **kwargs):
        super(AdjustBrightness, self).__init__(**kwargs)
        self.delta = delta
        self.is_random = is_random
        self.seed = seed

    def call(self, inputs, **kwargs):
        return adjust_brightness(images=inputs,
                                 delta=self.delta,
                                 is_random=self.is_random,
                                 seed=self.seed)


def adjust_contrast(images, contrast_factor, contrast_factor_max=None, is_random=False, seed=None):
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
        images: `tensor`. images tensor with 3 or more dimensions.
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
    """
    if is_random:
        assert contrast_factor_max is not None, '`contrast_factor_max` must be > contrast_factor'
        return tf.image.random_contrast(
            images, lower=contrast_factor, upper=contrast_factor_max, seed=seed)
    return tf.image.adjust_contrast(images, contrast_factor)


class AdjustContrast(BaseObject, Layer):
    """See `plx.image.adjust_contrast`'s docstring"""
    CONFIG = AdjustContrastConfig
    __doc__ = AdjustContrastConfig.__doc__

    def __init__(self, contrast_factor, contrast_factor_max=None, is_random=False, seed=None,
                 **kwargs):
        super(AdjustContrast, self).__init__(**kwargs)
        self.contrast_factor = contrast_factor
        self.contrast_factor_max = contrast_factor_max
        self.is_random = is_random
        self.seed = seed

    def call(self, inputs, **kwargs):
        return adjust_contrast(images=inputs,
                               contrast_factor=self.contrast_factor,
                               contrast_factor_max=self.contrast_factor_max,
                               is_random=self.is_random,
                               seed=self.seed)


def adjust_hue(images, delta, is_random=False, seed=None, name=None):
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
        images: RGB image or images. Size of the last dimension must be 3.
        delta: float.  How much to add to the hue channel.
        is_random: `bool`, If True, adjust randomly.
        seed: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.
        name: A name for this operation (optional).

    Returns:
        Adjusted image(s), same shape and DType as `image`.
    """
    if is_random:
        return tf.image.random_hue(images, max_delta=delta, seed=seed)
    return tf.image.adjust_hue(images=images, delta=delta, name=name)


class AdjustHue(BaseObject, Layer):
    """See `plx.image.adjust_hue`'s docstring"""
    CONFIG = AdjustHueConfig
    __doc__ = AdjustHueConfig.__doc__

    def __init__(self, delta, is_random=False, seed=None, **kwargs):
        super(AdjustHue, self).__init__(**kwargs)
        self.delta = delta
        self.is_random = is_random
        self.seed = seed

    def call(self, inputs, **kwargs):
        return adjust_hue(images=inputs,
                          delta=self.delta,
                          is_random=self.is_random,
                          seed=self.seed,
                          name=self.name)


def adjust_saturation(images, saturation_factor, saturation_factor_max=None, is_random=False,
                      seed=None, name=None):
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
        images: RGB image or images. Size of the last dimension must be 3.
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
    """
    if is_random:
        return tf.image.random_saturation(
            images, lower=saturation_factor, upper=saturation_factor_max, seed=seed)
    return tf.image.adjust_saturation(images, saturation_factor=saturation_factor, name=name)


class AdjustSaturation(BaseObject, Layer):
    """See `plx.image.adjust_saturation`'s docstring"""
    CONFIG = AdjustSaturationConfig
    __doc__ = AdjustSaturationConfig.__doc__

    def __init__(self, saturation_factor, saturation_factor_max=None, is_random=False,
                 seed=None, **kwargs):
        super(AdjustSaturation, self).__init__(**kwargs)
        self.saturation_factor = saturation_factor
        self.saturation_factor_max = saturation_factor_max
        self.is_random = is_random
        self.seed = seed

    def call(self, inputs, **kwargs):
        return adjust_saturation(images=inputs,
                                 saturation_factor=self.saturation_factor,
                                 saturation_factor_max=self.saturation_factor_max,
                                 is_random=self.is_random,
                                 seed=self.seed,
                                 name=self.name)


def adjust_gamma(image, gamma=1, gain=1):
    """Performs Gamma Correction on the input image.
    Also known as Power Law Transform. This function transforms the
    input image pixelwise according to the equation Out = In**gamma
    after scaling each pixel to the range 0 to 1.
    (A mirror to tf.image adjust_gamma)

    Args:
        image : A Tensor.
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
    """
    return tf.image.adjust_gamma(image, gamma, gain)


class AdjustGamma(BaseObject, Layer):
    """See `plx.image.adjust_gamma`'s docstring"""
    CONFIG = AdjustGammaConfig
    __doc__ = AdjustGammaConfig.__doc__

    def __init__(self, gamma=1, gain=1, **kwargs):
        super(AdjustGamma, self).__init__(**kwargs)
        self.gamma = gamma
        self.gain = gain

    def call(self, inputs, **kwargs):
        return adjust_gamma(image=inputs, gamma=self.gamma, gain=self.gain)


def standardize(images):
    """Linearly scales `image` to have zero mean and unit norm.
    (A mirror to tf.image per_image_standardization)

    This op computes `(x - mean) / adjusted_stddev`, where `mean` is the average
    of all values in image, and
    `adjusted_stddev = max(stddev, 1.0/sqrt(image.NumElements()))`.

    `stddev` is the standard deviation of all values in `image`. It is capped
    away from zero to protect against division by 0 when handling uniform images.

    Args:
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
                3-D Tensor of shape `[height, width, channels]`.

    Returns:
        The standardized image with same shape as `image`.

    Raises:
        ValueError: if the shape of 'image' is incompatible with this function.
    """
    images_shape = get_shape(images)
    if len(images_shape) > 4:
        ValueError("'image' must have either 3 or 4 dimensions, "
                   "received `{}`.".format(images_shape))

    if len(images_shape) == 4:
        return tf.map_fn(tf.image.per_image_standardization, images)
    return tf.image.per_image_standardization(images)


class Standardization(BaseObject, Layer):
    """See `plx.image.standardize`'s docstring"""
    CONFIG = StandardizationConfig
    __doc__ = StandardizationConfig.__doc__

    def call(self, inputs, **kwargs):
        return standardize(images=inputs)


def draw_bounding_boxes(images, boxes, name=None):
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
        images: A `Tensor`. Must be one of the following types: `float32`, `half`.
            4-D with shape `[batch, height, width, depth]`. A batch of images.
        boxes: A `Tensor` of type `float32`.
            3-D with shape `[batch, num_bounding_boxes, 4]` containing bounding boxes.
        name: A name for the operation (optional).

    Returns:
        A `Tensor`. Has the same type as `images`.
        4-D with the same shape as `images`. The batch of input images with
        bounding boxes drawn on the images.
    """
    return tf.image.draw_bounding_boxes(images=images, boxes=boxes, name=name)


class DrawBoundingBoxes(BaseObject, Layer):
    """See `plx.image.draw_bounding_boxes`'s docstring"""
    CONFIG = DrawBoundingBoxesConfig
    __doc__ = DrawBoundingBoxesConfig.__doc__

    def __init__(self, boxes, **kwargs):
        super(DrawBoundingBoxes, self).__init__(**kwargs)
        self.boxes = boxes

    def call(self, inputs, **kwargs):
        return draw_bounding_boxes(images=inputs, boxes=self.boxes, name=self.name)


def non_max_suppression(boxes, scores, max_output_size, iou_threshold=None, name=None):
    """Greedily selects a subset of bounding boxes in descending order of score,
    pruning away boxes that have high intersection-over-union (IOU) overlap
    with previously selected boxes.  Bounding boxes are supplied as
    [y1, x1, y2, x2], where (y1, x1) and (y2, x2) are the coordinates of any
    diagonal pair of box corners and the coordinates can be provided as normalized
    (i.e., lying in the interval [0, 1]) or absolute.  Note that this algorithm
    is agnostic to where the origin is in the coordinate system.  Note that this
    algorithm is invariant to orthogonal transformations and translations
    of the coordinate system; thus translating or reflections of the coordinate
    system result in the same boxes being selected by the algorithm.

    (A mirror to tf.image non_max_suppression)

    The output of this operation is a set of integers indexing into the input
    collection of bounding boxes representing the selected boxes.  The bounding
    box coordinates corresponding to the selected indices can then be obtained
    using the `tf.gather operation`.  For example:

    Examples:
    ```python
    >>> selected_indices = tf.image.non_max_suppression(
    ...     boxes, scores, max_output_size, iou_threshold)
    >>> selected_boxes = tf.gather(boxes, selected_indices)
    ```

    Args:
        boxes: A `Tensor` of type `float32`.
            A 2-D float tensor of shape `[num_boxes, 4]`.
        scores: A `Tensor` of type `float32`.
            A 1-D float tensor of shape `[num_boxes]` representing a single
            score corresponding to each box (each row of boxes).
        max_output_size: A `Tensor` of type `int32`.
            A scalar integer tensor representing the maximum number of
            boxes to be selected by non max suppression.
        iou_threshold: An optional `float`. Defaults to `0.5`.
            A float representing the threshold for deciding whether boxes
            overlap too much with respect to IOU.
        name: A name for the operation (optional).

    Returns:
        A `Tensor` of type `int32`.
        A 1-D integer tensor of shape `[M]` representing the selected
        indices from the boxes tensor, where `M <= max_output_size`.
    """
    return tf.image.non_max_suppression(
        boxes=boxes, scores=scores, max_output_size=max_output_size,
        iou_threshold=iou_threshold, name=name)


def sample_distorted_bounding_box(image_size, bounding_boxes, seed=None,
                                  seed2=None, min_object_covered=None,
                                  aspect_ratio_range=None, area_range=None,
                                  max_attempts=None,
                                  use_image_if_no_bounding_boxes=None,
                                  name=None):
    """Generate a single randomly distorted bounding box for an image.

    Bounding box annotations are often supplied in addition to ground-truth labels
    in image recognition or object localization tasks. A common technique for
    training such a system is to randomly distort an image while preserving
    its content, i.e. *data augmentation*. This Op outputs a randomly distorted
    localization of an object, i.e. bounding box, given an `image_size`,
    `bounding_boxes` and a series of constraints.

    (A mirror to tf.image sample_distorted_bounding_box)

    The output of this Op is a single bounding box that may be used to crop the
    original image. The output is returned as 3 tensors: `begin`, `size` and
    `bboxes`. The first 2 tensors can be fed directly into `tf.slice` to crop the
    image. The latter may be supplied to `tf.image.draw_bounding_boxes` to visualize
    what the bounding box looks like.

    Bounding boxes are supplied and returned as `[y_min, x_min, y_max, x_max]`. The
    bounding box coordinates are floats in `[0.0, 1.0]` relative to the width and
    height of the underlying image.

    Examples:
    ```python
    >>> # Generate a single distorted bounding box.
    >>> begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(
    ...     tf.shape(image), bounding_boxes=bounding_boxes)

    >>> # Draw the bounding box in an image summary.
    >>> image_with_box = tf.image.draw_bounding_boxes(
    ...     tf.expand_dims(image, 0), bbox_for_draw)
    >>> tf.image_summary('images_with_box', image_with_box)

    >>> # Employ the bounding box to distort the image.
    >>> distorted_image = tf.slice(image, begin, size)
    ```

    Note that if no bounding box information is available, setting
    `use_image_if_no_bounding_boxes = true` will assume there is a single implicit
    bounding box covering the whole image. If `use_image_if_no_bounding_boxes` is
    false and no bounding boxes are supplied, an error is raised.

    Args:
        image_size: A `Tensor`. Must be one of the following types:
            `uint8`, `int8`, `int16`, `int32`, `int64`.
            1-D, containing `[height, width, channels]`.
        bounding_boxes: A `Tensor` of type `float32`.
            3-D with shape `[batch, N, 4]` describing the N bounding boxes
            associated with the image.
        seed: An optional `int`. Defaults to `0`.
            If either `seed` or `seed2` are set to non-zero, the random number
            generator is seeded by the given `seed`.  Otherwise, it is seeded by a random seed.
        seed2: An optional `int`. Defaults to `0`. A second seed to avoid seed collision.
        min_object_covered: An optional `float`. Defaults to `0.1`.
            The cropped area of the image must contain at least this
            fraction of any bounding box supplied. The value of this parameter should be
            non-negative. In the case of 0, the cropped area does not need to overlap
            any of the bounding boxes supplied.
        aspect_ratio_range: An optional list of `floats`. Defaults to `[0.75, 1.33]`.
            The cropped area of the image must have an aspect ratio =
            width / height within this range.
        area_range: An optional list of `floats`. Defaults to `[0.05, 1]`.
            The cropped area of the image must contain a fraction of the
            supplied image within in this range.
        max_attempts: An optional `int`. Defaults to `100`.
            Number of attempts at generating a cropped region of the image
            of the specified constraints. After `max_attempts` failures, return the entire image.
        use_image_if_no_bounding_boxes: An optional `bool`. Defaults to `False`.
            Controls behavior if no bounding boxes supplied.
            If true, assume an implicit bounding box covering the whole input. If false,
            raise an error.
        name: A name for the operation (optional).

    Returns:
        A tuple of `Tensor` objects (begin, size, bboxes).
        begin: A `Tensor`. Has the same type as `image_size`. 1-D, containing
            `[offset_height, offset_width, 0]`. Provide as input to `tf.slice`.
        size: A `Tensor`. Has the same type as `image_size`. 1-D, containing
            `[target_height, target_width, -1]`. Provide as input to `tf.slice`.
        bboxes: A `Tensor` of type `float32`. 3-D with shape `[1, 1, 4]` containing
            the distorted bounding box. Provide as input to `tf.image.draw_bounding_boxes`.
    """
    return tf.image.sample_distorted_bounding_box(
        image_size, bounding_boxes, seed, seed2, min_object_covered, aspect_ratio_range,
        area_range, max_attempts, use_image_if_no_bounding_boxes, name)


def total_variation(images, name=None):
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
        images: 4-D Tensor of shape `[batch, height, width, channels]` or
                3-D Tensor of shape `[height, width, channels]`.

        name: A name for the operation (optional).

    Raises:
        ValueError: if images.shape is not a 3-D or 4-D vector.

    Returns:
        The total variation of `images`.

        If `images` was 4-D, return a 1-D float Tensor of shape `[batch]` with the
        total variation for each image in the batch.
        If `images` was 3-D, return a scalar float with the total variation for
        that image.
    """
    return tf.image.total_variation(images=images, name=name)


class TotalVariation(BaseObject, Layer):
    """See `plx.image.total_variation`'s docstring"""
    CONFIG = TotalVariationConfig
    __doc__ = TotalVariationConfig.__doc__

    def call(self, inputs, **kwargs):
        return total_variation(images=inputs, name=self.name)


IMAGE_PROCESSORS = OrderedDict([
    ('Resize', Resize),
    ('CentralCrop', CentralCrop),
    ('RandomCrop', RandomCrop),
    ('ExtractGlimpse', ExtractGlimpse),
    ('ToBoundingBox', ToBoundingBox),
    ('Flip', Flip),
    ('Transpose', Transpose),
    ('Rotate90', Rotate90),
    ('ConvertColorSpace', ConvertColorSpace),
    ('ConvertImagesDtype', ConvertImagesDtype),
    ('AdjustBrightness', AdjustBrightness),
    ('AdjustContrast', AdjustContrast),
    ('AdjustHue', AdjustHue),
    ('AdjustSaturation', AdjustSaturation),
    ('AdjustGamma', AdjustGamma),
    ('Standardization', Standardization),
    ('DrawBoundingBoxes', DrawBoundingBoxes),
    ('TotalVariation', TotalVariation),
])
