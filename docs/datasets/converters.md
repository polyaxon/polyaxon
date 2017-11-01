<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/converters/image_converters.py#L16)</span>
## ImageReader

```python
polyaxon.datasets.converters.image_converters.ImageReader(channels=3)
```

Base ImageReader class that provides an operation to read/encode/decode an image.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/converters/image_converters.py#L32)</span>
## PNGImageReader

```python
polyaxon.datasets.converters.image_converters.PNGImageReader(channels=3)
```

A png image class reader

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/converters/image_converters.py#L38)</span>
## PNGNumpyImageReader

```python
polyaxon.datasets.converters.image_converters.PNGNumpyImageReader(shape=None)
```

A numpy png image class reader

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/converters/image_converters.py#L53)</span>
## JPGNumpyImageReader

```python
polyaxon.datasets.converters.image_converters.JPGNumpyImageReader(shape=None)
```

A jpeg numpy image class reader

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/converters/image_converters.py#L67)</span>
## JPEGImageReader

```python
polyaxon.datasets.converters.image_converters.JPEGImageReader(channels=3)
```

A jpeg image class reader

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/converters/image_converters.py#L73)</span>
## ImagesToTFExampleConverter

```python
polyaxon.datasets.converters.image_converters.ImagesToTFExampleConverter(classes, colorspace, image_format, channels, image_reader=None, height=None, width=None, store_filenames=False)
```

Converts images to a TFRecords of TF-Example protos.

Each record is TF-Example protocol buffer which contain a single image and label.

- __Args__:

	- __classes__: `dict` or `list`. The data classes.

		e.g. ['zero', 'one', 'two', ...] or {0: 'cats', 1: 'dogs'}
	- __colorspace__: `str`. The color space of the images, 'rgb', 'grayscale' ...

	- __image_format__: `str`. The format of the images, 'png', 'jpeg'.

	- __channels__: `int`. The number of channels of the images, e.g. 1, 3.

	- __image_reader__: `ImageReader` instance. If `None` an image reader is created automatically

		based on the `image_format`.
	- __height__: `int`. If provided the the height per image will not be stored in the TFRecord,

		only in the meta_data file.
	- __width__: `int`. If provided the the width per image will not be stored in the TFRecord,

		only in the meta_data file.
	- __store_filenames__: `bool`. If `True` the filename of the image will be stored as a feature.

