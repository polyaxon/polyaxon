# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

from six.moves import xrange

from collections import Mapping

import tensorflow as tf

from polyaxon.datasets.converters.base import BaseConverter


class ImageReader(object):
    """Base ImageReader class that provides an operation to read/encode/decode an image."""
    def __init__(self, channels=3):
        self._placeholder = tf.placeholder(dtype=tf.string)
        self._image = self.decoder(channels)

    def decoder(self, channels):
        raise NotImplementedError

    def read(self, session, image_data, processing_fn=None):
        _image = self._image
        if processing_fn:
            _image = processing_fn(session, _image)
        return image_data, session.run(_image, feed_dict={self._placeholder: image_data})


class PNGImageReader(ImageReader):
    """A png image class reader"""
    def decoder(self, channels):
        return tf.image.decode_png(self._placeholder, channels=channels)


class PNGNumpyImageReader(ImageReader):
    """A numpy png image class reader"""

    def __init__(self, shape=None):
        self._placeholder = tf.placeholder(dtype=tf.uint8, shape=shape)
        self._image = tf.image.encode_png(self._placeholder)

    def decoder(self, channels):
        pass

    def read(self, session, image_data, processing_fn=None):
        _, image = super(PNGNumpyImageReader, self).read(session, image_data, processing_fn)
        return image, image


class JPGNumpyImageReader(ImageReader):
    """A jpeg numpy image class reader"""
    def __init__(self, shape=None):
        self._placeholder = tf.placeholder(dtype=tf.uint8, shape=shape)
        self._image = tf.image.encode_jpeg(self._placeholder)

    def decoder(self, channels):
        pass

    def read(self, session, image_data, processing_fn=None):
        _, image = super(JPGNumpyImageReader, self).read(session, image_data, processing_fn)
        return image, image


class JPEGImageReader(ImageReader):
    """A jpeg image class reader"""
    def decoder(self, channels):
        return tf.image.decode_jpeg(self._placeholder, channels=channels)


class ImagesToTFExampleConverter(BaseConverter):
    """Converts images to a TFRecords of TF-Example protos.

    Each record is TF-Example protocol buffer which contain a single image and label.

    Args:
        classes: `dict` or `list`. The data classes.
            e.g. ['zero', 'one', 'two', ...] or {0: 'cats', 1: 'dogs'}
        colorspace: `str`. The color space of the images, 'rgb', 'grayscale' ...
        image_format: `str`. The format of the images, 'png', 'jpeg'.
        channels: `int`. The number of channels of the images, e.g. 1, 3.
        image_reader: `ImageReader` instance. If `None` an image reader is created automatically
            based on the `image_format`.
        height: `int`. If provided the the height per image will not be stored in the TFRecord,
            only in the meta_data file.
        width: `int`. If provided the the width per image will not be stored in the TFRecord,
            only in the meta_data file.
        store_filenames: `bool`. If `True` the filename of the image will be stored as a feature.
    """
    def __init__(self, classes, colorspace, image_format, channels, image_reader=None,
                 height=None, width=None, store_filenames=False):
        if image_reader:
            self.image_reader = image_reader
        else:
            if image_format == 'png':
                self.image_reader = PNGImageReader(channels=channels)
            elif image_format == 'jpeg':
                self.image_reader = JPEGImageReader(channels=channels)

        if isinstance(classes, Mapping):
            self.classes = list(classes.values())
            self.labels_to_classes = classes
        elif isinstance(classes, list):
            assert len(set(classes)) == len(classes), '`classes` must contain unique values.'
            self.classes = classes
            self.labels_to_classes = dict(zip(range(len(classes)), classes))
        else:
            raise TypeError('`classes` type is unsupported, received `{}`'.format(type(classes)))

        self.classes_to_labels = {v: k for k, v in self.labels_to_classes.items()}
        self.colorspace = colorspace
        self.image_format = image_format
        self.channels = channels
        self.store_filenames = store_filenames
        self.height = height
        self.width = width

    def get_meta_data(self):
        return {
            'classes': self.classes,
            'num_classes': len(self.classes),
            'labels_to_classes': self.labels_to_classes,
            'colorspace': self.colorspace,
            'image_format': self.image_format,
            'channels': self.channels,
            'height': self.height,
            'width': self.width
        }

    def get_image_features(self, image):
        height = image.shape[0]
        width = image.shape[1]
        assert image.shape[2] == self.channels
        if self.height:
            assert height == self.height
        if self.width:
            assert height == self.width
        return height, width

    def create_example(self, image_data, encoded_image, label, filename=None):
        if hasattr(encoded_image, 'shape'):
            height, width = self.get_image_features(image=encoded_image)
        else:
            # the image could a bytes string
            height, width = self.height, self.width

        if height is None:
            raise ValueError('No `height` will be stored for the images. '
                             'If all images have the `height`, please provide '
                             'the `height`  at instantiation.')

        if width is None:
            raise ValueError('No `width` will be stored for the images. '
                             'If all images have the `width`, please provide '
                             'the `width`  at instantiation.')

        features = {
            'image/class/label': self.to_int64_feature(label),
            'image/encoded': self.to_bytes_feature(tf.compat.as_bytes(image_data)),
            'image/width': self.to_int64_feature(width),
            'image/height': self.to_int64_feature(height),
            'image/format': self.to_bytes_feature(self.image_format.encode()),
            'image/colorspace': self.to_bytes_feature(tf.compat.as_bytes(self.colorspace)),
            'image/channels': self.to_int64_feature(self.channels),
        }
        if self.store_filenames:
            filename_feature = self.to_bytes_feature(tf.compat.as_bytes(os.path.basename(filename)))
            features['image/filename'] = filename_feature

        return tf.train.Example(features=tf.train.Features(feature=features))

    def convert(self, session, writer, images, labels, total_num_items, start_index=0,
                filenames=None, processing_fn=None, post_processing_fn=None):

        if self.store_filenames and not filenames:
            raise ValueError('`filenames` is required to store the filename in TF-Example.'
                             'Either provide a list of `filenames` or '
                             'set `store_filenames` to `False`')

        for i in xrange(start_index, len(images)):
            sys.stdout.write('\r>> Converting image %d/%d' % (i + 1, total_num_items))
            sys.stdout.flush()

            image_data, encoded_image = self.image_reader.read(
                session=session, image_data=images[i], processing_fn=processing_fn)
            if post_processing_fn:
                _, image_data = post_processing_fn(session, encoded_image)
            example = self.create_example(image_data, encoded_image, labels[i],
                                          filenames[i] if self.store_filenames else None)
            writer.write(example.SerializeToString())
