<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L91)</span>
## Resize

```python
polyaxon.processing.image.Resize(height, width, method=None, align_corners=False)
```

See `plx.image.resize`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L152)</span>
## CentralCrop

```python
polyaxon.processing.image.CentralCrop(central_fraction)
```

See `plx.image.central_crop`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L190)</span>
## RandomCrop

```python
polyaxon.processing.image.RandomCrop(height, width)
```

See `plx.image.random_crop`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L255)</span>
## ExtractGlimpse

```python
polyaxon.processing.image.ExtractGlimpse(size, offsets, centered=None, normalized=None, uniform_noise=None)
```

See `plx.image.extract_glimpse`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L331)</span>
## ToBoundingBox

```python
polyaxon.processing.image.ToBoundingBox(offset_height, offset_width, target_height, target_width, method='crop')
```

See `plx.image.to_bounding_box`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L401)</span>
## Flip

```python
polyaxon.processing.image.Flip(axis=0, is_random=False, seed=None)
```

See `plx.image.flip`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L443)</span>
## Transpose

```python
tensorflow.contrib.keras.python.keras.engine.topology.Transpose()
```

See `plx.image.transpose`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L486)</span>
## Rotate90

```python
polyaxon.processing.image.Rotate90(k=1, is_random=False, seed=None)
```

See `plx.image.rotate90`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L563)</span>
## ConvertColorSpace

```python
polyaxon.processing.image.ConvertColorSpace(from_space, to_space)
```

See `plx.image.convert_color_space`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L620)</span>
## ConvertImagesDtype

```python
polyaxon.processing.image.ConvertImagesDtype(dtype, saturate=False)
```

See `plx.image.convert_images_dtype`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L893)</span>
## AdjustGamma

```python
polyaxon.processing.image.AdjustGamma(gamma=1, gain=1)
```

See `plx.image.adjust_gamma`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L938)</span>
## Standardization

```python
tensorflow.contrib.keras.python.keras.engine.topology.Standardization()
```

See `plx.image.standardize`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L977)</span>
## DrawBoundingBoxes

```python
polyaxon.processing.image.DrawBoundingBoxes(boxes)
```

See `plx.image.draw_bounding_boxes`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L1169)</span>
## TotalVariation

```python
tensorflow.contrib.keras.python.keras.engine.topology.TotalVariation()
```

See `plx.image.total_variation`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L668)</span>
## AdjustBrightness

```python
polyaxon.processing.image.AdjustBrightness(delta, is_random=False, seed=None)
```

See `plx.image.adjust_brightness`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L730)</span>
## AdjustContrast

```python
polyaxon.processing.image.AdjustContrast(contrast_factor, contrast_factor_max=None, is_random=False, seed=None)
```

See `plx.image.adjust_contrast`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L783)</span>
## AdjustHue

```python
polyaxon.processing.image.AdjustHue(delta, is_random=False, seed=None)
```

See `plx.image.adjust_hue`'s docstring

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/image.py#L845)</span>
## AdjustSaturation

```python
polyaxon.processing.image.AdjustSaturation(saturation_factor, saturation_factor_max=None, is_random=False, seed=None)
```

See `plx.image.adjust_saturation`'s docstring

----

## resize


```python
resize(images, height, width, method=None, align_corners=False)
```


Resize `images` to `size` using the specified `method`.
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

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	3-D Tensor of shape `[height, width, channels]`.
	- __height__: int32 Target height.
	- __width__: int32 Target width.
	- __method__: ResizeMethod.  Defaults to `ResizeMethod.BILINEAR`.
	Possible values: BILINEAR, NEAREST_NEIGHBOR, BICUBIC, AREA
	- __align_corners__: bool. If true, exactly align all 4 corners of the input and output.
	Only used if method is not None. Defaults to `false`.

- __Raises__:
	- __ValueError__: if the shape of `images` is incompatible with the
	shape arguments to this function.
	- __ValueError__: if `size` has invalid shape or type.
	- __ValueError__: if an unsupported resize method is specified.

- __Returns__:
	If `images` was 4-D, a 4-D float Tensor of shape
	`[batch, new_height, new_width, channels]`.
	If `images` was 3-D, a 3-D float Tensor of shape
	`[new_height, new_width, channels]`.


----

## central_crop


```python
central_crop(images, central_fraction)
```


Crop the central region of the image.
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

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	3-D Tensor of shape `[height, width, channels]`.
	- __central_fraction__: float (0, 1], fraction of size to crop

- __Raises__:
	- __ValueError__: if central_crop_fraction is not within (0, 1].

- __Returns__:
	If `images` was 4-D, a 4-D float Tensor of shape
	`[batch, new_height, new_width, channels]`.
	If `images` was 3-D, a 3-D float Tensor of shape
	`[new_height, new_width, channels]`.


----

## random_crop


```python
random_crop(images, height, width)
```


Randomly crops an image/images to a given size.

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	3-D Tensor of shape `[height, width, channels]`.
	- __height__: `float`. The height to crop to.
	- __width__: `float`. The width to crop to.

- __Returns__:
	If `images` was 4-D, a 4-D float Tensor of shape
	`[batch, new_height, new_width, channels]`.
	If `images` was 3-D, a 3-D float Tensor of shape
	`[new_height, new_width, channels]`.


----

## extract_glimpse


```python
extract_glimpse(images, size, offsets, centered=None, normalized=None, uniform_noise=None, name=None)
```


Extracts a glimpse from the input tensor.
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

- __Args__:
	- __images__: A `Tensor` of type `float32`.
	A 4-D float tensor of shape `[batch_size, height, width, channels]`.
	- __size__: A `Tensor` of type `int32`.
	A 1-D tensor of 2 elements containing the size of the glimpses to extract.
	The glimpse height must be specified first, following by the glimpse width.
	- __offsets__: A `Tensor` of type `float32`.
	A 2-D integer tensor of shape `[batch_size, 2]` containing
	the y, x locations of the center of each window.
	- __centered__: An optional `bool`. Defaults to `True`.
	indicates if the offset coordinates are centered relative to the image,
	in which case the (0, 0) offset is relative to the center of the input images.
	If false, the (0,0) offset corresponds to the upper left corner of the input images.
	- __normalized__: An optional `bool`. Defaults to `True`.
	indicates if the offset coordinates are normalized.
	- __uniform_noise__: An optional `bool`. Defaults to `True`.
	indicates if the noise should be generated using a
	uniform distribution or a Gaussian distribution.
	- __name__: A name for the operation (optional).

- __Returns__:
	A `Tensor` of type `float32`.
	A tensor representing the glimpses `[batch_size, glimpse_height, glimpse_width, channels]`.


----

## to_bounding_box


```python
to_bounding_box(images, offset_height, offset_width, target_height, target_width, method='crop')
```


Pad/Crop `image` with zeros to the specified `height` and `width`.
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

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	   3-D Tensor of shape `[height, width, channels]`.
	- __offset_height__:
	* pad: Number of rows of zeros to add on top.
	* crop: Vertical coordinate of the top-left corner of the result the input.
	- __offset_width__:
	* pad: Number of columns of zeros to add on the left.
	* crop: Horizontal coordinate of the top-left corner of the result in the input.
	- __target_height__: Height of output image.
	- __target_width__: Width of output image.
	- __method__: `crop` or `pad`

- __Returns__:
	If `image` was 4-D, a 4-D float Tensor of shape
	`[batch, target_height, target_width, channels]`
	If `image` was 3-D, a 3-D float Tensor of shape
	`[target_height, target_width, channels]`

- __Raises__:
	- __ValueError__: If the shape of `image` is incompatible with the `offset_*` or
	`target_*` arguments, or either `offset_height` or `offset_width` is negative.


----

## flip


```python
flip(images, axis=0, is_random=False, seed=None)
```


Flip (randomly) an image/images.
(A mirror to tf.image flip_left_right, flip_up_down, random_flip_left_right, and
random_flip_up_down)

 if axis is 0:
	* flip horizontally (left to right)
 if axis is 1:
	* vertically (upside down).

Outputs the contents of `images` flipped along the given axis.

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	3-D Tensor of shape `[height, width, channels]`.
	- __axis__: `int`. 0 for horizontal, 1 for vertical
	- __is_random__: `bool`, If True, flip randomly.
	- __seed__: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.

- __Returns__:
	If `image` was 4-D, a 4-D float Tensor of shape
	`[batch, target_height, target_width, channels]`
	If `image` was 3-D, a 3-D float Tensor of shape
	`[target_height, target_width, channels]

- __Raises__:
	- __ValueError__: if the shape of `image` not supported.


----

## transpose


```python
transpose(images)
```


Transpose an image/images by swapping the first and second dimension.
(A mirror to tf.image transpose_image)

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	3-D Tensor of shape `[height, width, channels]`.

- __Returns__:
	If `image` was 4-D, a 4-D float Tensor of shape
	`[batch, target_height, target_width, channels]`
	If `image` was 3-D, a 3-D float Tensor of shape
	`[target_height, target_width, channels]

- __Raises__:
	- __ValueError__: if the shape of `image` not supported.


----

## rotate90


```python
rotate90(images, k=1, is_random=False, seed=None, name=None)
```


Rotate (randomly) images counter-clockwise by 90 degrees.
(A mirror to tf.image rot90)

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
	3-D Tensor of shape `[height, width, channels]`.
	- __k__: A scalar integer. The number of times the image is rotated by 90 degrees.
	- __is_random__: `bool`, If True, adjust randomly.
	- __seed__: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.
	- __name__: A name for this operation (optional).

- __Returns__:
	If `image` was 4-D, a 4-D float Tensor of shape
	`[batch, target_height, target_width, channels]`
	If `image` was 3-D, a 3-D float Tensor of shape
	`[target_height, target_width, channels]

- __Raises__:
	- __ValueError__: if the shape of `image` not supported.


----

## convert_color_space


```python
convert_color_space(images, from_space, to_space, name=None)
```


Converts one or more images from RGB to Grayscale.
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

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]`
	- __from_space__: The color to convert from.
	- __to_space__: The color space to convert to.
	- __name__: A name for the operation (optional).

- __Returns__:
	The converted image(s).


----

## convert_images_dtype


```python
convert_images_dtype(images, dtype, saturate=False, name=None)
```


Convert image(s) to `dtype`, scaling its values if needed.
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

  - __Args__:
	- __images__: An image.
	- __dtype__: A `DType` to convert `image` to.
	- __saturate__: If `True`, clip the input before casting (if necessary).
	- __name__: A name for this operation (optional).

  - __Returns__:
	`image`, converted to `dtype`.
  

----

## adjust_brightness


```python
adjust_brightness(images, delta, is_random=False, seed=None)
```


Adjust (randomly) the brightness of RGB or Grayscale images.
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

- __Args__:
	- __images__: A tensor.
	- __delta__: `float`. Amount to add to the pixel values.
	- __is_random__: `bool`, If True, adjust randomly.
	- __seed__: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.

- __Returns__:
	A brightness-adjusted tensor of the same shape and type as `images`.


----

## adjust_contrast


```python
adjust_contrast(images, contrast_factor, contrast_factor_max=None, is_random=False, seed=None)
```


Adjust (randomly) the contrast of RGB or grayscale images by contrast factor.
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

- __Args__:
	- __images__: `tensor`. images tensor with 3 or more dimensions.
	- __contrast_factor__: `float`.  Lower bound for the random contrast factor.
	- __contrast_factor_max__: `float`.  Upper bound for the random contrast factor.
	Used for random adjustment.
	- __is_random__: `bool`, If True, adjust randomly.
	- __seed__: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.

- __Returns__:
	The contrast-adjusted tensor.

- __Raises__:
	- __ValueError__: if `contrast_factor_max <= contrast_factor`
		if `contrast_factor < 0`
		if `contrast_factor_max` is None (for random.)


----

## adjust_hue


```python
adjust_hue(images, delta, is_random=False, seed=None, name=None)
```


Adjust (randomly) hue of an RGB images.
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

- __Args__:
	- __images__: RGB image or images. Size of the last dimension must be 3.
	- __delta__: float.  How much to add to the hue channel.
	- __is_random__: `bool`, If True, adjust randomly.
	- __seed__: A Python integer. Used to create a random seed. See @{tf.set_random_seed}.
	- __name__: A name for this operation (optional).

- __Returns__:
	Adjusted image(s), same shape and DType as `image`.


----

## adjust_saturation


```python
adjust_saturation(images, saturation_factor, saturation_factor_max=None, is_random=False, seed=None, name=None)
```


Adjust (randomly) saturation of RGB images.
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

- __Args__:
	- __images__: RGB image or images. Size of the last dimension must be 3.
	- __saturation_factor__: float.  Lower bound for the random saturation factor.
	- __saturation_factor_max__: float.  Upper bound for the random saturation factor.
	- __is_random__: `bool`, If True, adjust randomly.
	- __seed__: An operation-specific seed. It will be used in conjunction
	  with the graph-level seed to determine the real seeds that will be
	  used in this operation. Please see the documentation of
	  set_random_seed for its interaction with the graph-level random seed.
	- __name__: A name for this operation (optional).

- __Returns__:
	Adjusted image(s), same shape and DType as `image`.

- __Raises__:

	- __ValueError__: if `saturation_factor_max <= saturation_factor`
		if `saturation_factor < 0`
		if `saturation_factor_max is None (for random.)`


----

## adjust_gamma


```python
adjust_gamma(image, gamma=1, gain=1)
```


Performs Gamma Correction on the input image.
Also known as Power Law Transform. This function transforms the
input image pixelwise according to the equation Out = In**gamma
after scaling each pixel to the range 0 to 1.
(A mirror to tf.image adjust_gamma)

- __Args__:
	image : A Tensor.
	gamma : A scalar. Non negative real number.
	gain  : A scalar. The constant multiplier.

- __Returns__:
	A Tensor. Gamma corrected output image.

- __Notes__:
	For gamma greater than 1, the histogram will shift towards left and
	the output image will be darker than the input image.
	For gamma less than 1, the histogram will shift towards right and
	the output image will be brighter than the input image.

- __References__:
	[1] http://en.wikipedia.org/wiki/Gamma_correction


----

## standardize


```python
standardize(images)
```


Linearly scales `image` to have zero mean and unit norm.
(A mirror to tf.image per_image_standardization)

This op computes `(x - mean) / adjusted_stddev`, where `mean` is the average
of all values in image, and
`adjusted_stddev = max(stddev, 1.0/sqrt(image.NumElements()))`.

`stddev` is the standard deviation of all values in `image`. It is capped
away from zero to protect against division by 0 when handling uniform images.

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
		3-D Tensor of shape `[height, width, channels]`.

- __Returns__:
	The standardized image with same shape as `image`.

- __Raises__:
	- __ValueError__: if the shape of 'image' is incompatible with this function.



----

## draw_bounding_boxes


```python
draw_bounding_boxes(images, boxes, name=None)
```


Draw bounding boxes on a batch of images.
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

- __Args__:
	- __images__: A `Tensor`. Must be one of the following types: `float32`, `half`.
	4-D with shape `[batch, height, width, depth]`. A batch of images.
	- __boxes__: A `Tensor` of type `float32`.
	3-D with shape `[batch, num_bounding_boxes, 4]` containing bounding boxes.
	- __name__: A name for the operation (optional).

- __Returns__:
	A `Tensor`. Has the same type as `images`.
	4-D with the same shape as `images`. The batch of input images with
	bounding boxes drawn on the images.


----

## non_max_suppression


```python
non_max_suppression(boxes, scores, max_output_size, iou_threshold=None, name=None)
```


Greedily selects a subset of bounding boxes in descending order of score,
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

- __Examples__:
```python
>>> selected_indices = tf.image.non_max_suppression(
... boxes, scores, max_output_size, iou_threshold)
>>> selected_boxes = tf.gather(boxes, selected_indices)
```

- __Args__:
	- __boxes__: A `Tensor` of type `float32`.
	A 2-D float tensor of shape `[num_boxes, 4]`.
	- __scores__: A `Tensor` of type `float32`.
	A 1-D float tensor of shape `[num_boxes]` representing a single
	score corresponding to each box (each row of boxes).
	- __max_output_size__: A `Tensor` of type `int32`.
	A scalar integer tensor representing the maximum number of
	boxes to be selected by non max suppression.
	- __iou_threshold__: An optional `float`. Defaults to `0.5`.
	A float representing the threshold for deciding whether boxes
	overlap too much with respect to IOU.
	- __name__: A name for the operation (optional).

- __Returns__:
	A `Tensor` of type `int32`.
	A 1-D integer tensor of shape `[M]` representing the selected
	indices from the boxes tensor, where `M <= max_output_size`.


----

## sample_distorted_bounding_box


```python
sample_distorted_bounding_box(image_size, bounding_boxes, seed=None, seed2=None, min_object_covered=None, aspect_ratio_range=None, area_range=None, max_attempts=None, use_image_if_no_bounding_boxes=None, name=None)
```


Generate a single randomly distorted bounding box for an image.

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

- __Examples__:
```python
>>> # Generate a single distorted bounding box.
>>> begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(
... tf.shape(image), bounding_boxes=bounding_boxes)

>>> # Draw the bounding box in an image summary.
>>> image_with_box = tf.image.draw_bounding_boxes(
... tf.expand_dims(image, 0), bbox_for_draw)
>>> tf.image_summary('images_with_box', image_with_box)

>>> # Employ the bounding box to distort the image.
>>> distorted_image = tf.slice(image, begin, size)
```

Note that if no bounding box information is available, setting
`use_image_if_no_bounding_boxes = true` will assume there is a single implicit
bounding box covering the whole image. If `use_image_if_no_bounding_boxes` is
false and no bounding boxes are supplied, an error is raised.

- __Args__:
	- __image_size__: A `Tensor`. Must be one of the following types:
	`uint8`, `int8`, `int16`, `int32`, `int64`.
	1-D, containing `[height, width, channels]`.
	- __bounding_boxes__: A `Tensor` of type `float32`.
	3-D with shape `[batch, N, 4]` describing the N bounding boxes
	associated with the image.
	- __seed__: An optional `int`. Defaults to `0`.
	If either `seed` or `seed2` are set to non-zero, the random number
	generator is seeded by the given `seed`.  Otherwise, it is seeded by a random seed.
	- __seed2__: An optional `int`. Defaults to `0`. A second seed to avoid seed collision.
	- __min_object_covered__: An optional `float`. Defaults to `0.1`.
	The cropped area of the image must contain at least this
	fraction of any bounding box supplied. The value of this parameter should be
	non-negative. In the case of 0, the cropped area does not need to overlap
	any of the bounding boxes supplied.
	- __aspect_ratio_range__: An optional list of `floats`. Defaults to `[0.75, 1.33]`.
	The cropped area of the image must have an aspect ratio =
	width / height within this range.
	- __area_range__: An optional list of `floats`. Defaults to `[0.05, 1]`.
	The cropped area of the image must contain a fraction of the
	supplied image within in this range.
	- __max_attempts__: An optional `int`. Defaults to `100`.
	Number of attempts at generating a cropped region of the image
	of the specified constraints. After `max_attempts` failures, return the entire image.
	- __use_image_if_no_bounding_boxes__: An optional `bool`. Defaults to `False`.
	Controls behavior if no bounding boxes supplied.
	If true, assume an implicit bounding box covering the whole input. If false,
	raise an error.
	- __name__: A name for the operation (optional).

- __Returns__:
	A tuple of `Tensor` objects (begin, size, bboxes).
	- __begin__: A `Tensor`. Has the same type as `image_size`. 1-D, containing
	`[offset_height, offset_width, 0]`. Provide as input to `tf.slice`.
	- __size__: A `Tensor`. Has the same type as `image_size`. 1-D, containing
	`[target_height, target_width, -1]`. Provide as input to `tf.slice`.
	- __bboxes__: A `Tensor` of type `float32`. 3-D with shape `[1, 1, 4]` containing
	the distorted bounding box. Provide as input to `tf.image.draw_bounding_boxes`.


----

## total_variation


```python
total_variation(images, name=None)
```


Calculate and return the total variation for one or more images.

(A mirror to tf.image total_variation)

The total variation is the sum of the absolute differences for neighboring
pixel-values in the input images. This measures how much noise is in the
images.

This can be used as a loss-function during optimization so as to suppress
noise in images. If you have a batch of images, then you should calculate
the scalar loss-value as the sum:
`loss = tf.reduce_sum(tf.image.total_variation(images))`

This implements the anisotropic 2-D version of the formula described here:

- __https__://en.wikipedia.org/wiki/Total_variation_denoising

- __Args__:
	- __images__: 4-D Tensor of shape `[batch, height, width, channels]` or
		3-D Tensor of shape `[height, width, channels]`.

	- __name__: A name for the operation (optional).

- __Raises__:
	- __ValueError__: if images.shape is not a 3-D or 4-D vector.

- __Returns__:
	The total variation of `images`.

	If `images` was 4-D, return a 1-D float Tensor of shape `[batch]` with the
	total variation for each image in the batch.
	If `images` was 3-D, return a scalar float with the total variation for
	that image.
