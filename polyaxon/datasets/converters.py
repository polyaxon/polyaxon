# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

from collections import Mapping

import tensorflow as tf


class ImageReader(object):
    decoder = None

    def __init__(self, channels=3):
        assert self.decoder is not None, '`decoder` cannot be `None`.'
        self._placeholder = tf.placeholder(dtype=tf.string)
        self._image = self.decoder(self._placeholder, channels=channels)

    def read(self, session, image_data, processing_fn=None):
        _image = self._image
        if processing_fn:
            _image = processing_fn(_image)
        return session.run(_image, feed_dict={self._placeholder: image_data})


class PNGImageReader(ImageReader):
    decoder = tf.image.decode_png
    

class PNGImageReaderNP(ImageReader):
    
    def __init__(self, shape):
        self._placeholder = tf.placeholder(dtype=tf.uint8, shape=shape)
        self._image = tf.image.encode_png(self._placeholder)


class JPEGImageReader(ImageReader):
    decoder = tf.image.decode_jpeg


class ImagesToTFExampleConverter(object):
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

    @staticmethod
    def to_int64_feature(values):
        """Returns a TF-Feature of int64s.

          Args:
            values: A scalar or list of values.

          Returns:
            a TF-Feature.
          """
        if not isinstance(values, list):
            values = [values]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

    @staticmethod
    def to_bytes_feature(values):
        """Returns a TF-Feature of bytes.

        Args:
            values: A string.

        Returns:
            a TF-Feature.
        """
        if not isinstance(values, list):
            values = [values]
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=values))

    @staticmethod
    def to_float_feature(values):
        """Returns a TF-Feature of floats.

        Args:
            values: A string.

        Returns:
            a TF-Feature.
        """
        if not isinstance(values, list):
            values = [values]
        return tf.train.Feature(float_list=tf.train.FloatList(value=values))

    def get_image_features(self, image):
        height = image.shape[1]
        width = image.shape[2]
        assert image.shape[3] == self.channels
        if self.height:
            assert height == self.height
        if self.width:
            assert height == self.width
        return height, width

    def create_example(self, image, label, filename):
        if hasattr(image, 'shape'):
            height, width = self.get_image_features(image=image)
        else:
            # the image could a bytes string
            height, width = self.height, self.width

        if height is None:
            raise ValueError('No `height` will be stored for the images. '
                             'If all images have the `height`, please provide '
                             'the `height`  at instantiation.')

        if self.width is None:
            raise ValueError('No `width` will be stored for the images. '
                             'If all images have the `width`, please provide '
                             'the `width`  at instantiation.')

        features = {'image/class/label': self.to_int64_feature(label),
                    'image/encoded': self.to_bytes_feature(tf.compat.as_bytes(image)),
                    'image/width': self.to_int64_feature(width),
                    'image/height': self.to_int64_feature(height),
                    'image/format': self.to_bytes_feature(self.image_format.encode())}
        if self.store_filenames:
            filename_feature = self.to_bytes_feature(tf.compat.as_bytes(os.path.basename(filename)))
            features['image/filename'] = filename_feature

        return tf.train.Example(features=tf.train.Features(feature=features))

    def convert(self, session, writer, images, labels, total_num_items, start_index=0,
                filenames=None, processing_fn=None):

        if self.store_filenames and not filenames:
            raise ValueError('`filenames` is required to store the filename in TF-Example.'
                             'Either provide a list of `filenames` or '
                             'set `store_filenames` to `False`')

        for i in range(start_index, len(images)):
            sys.stdout.write('\r>> Converting image %d/%d' % (i + 1, total_num_items))
            sys.stdout.flush()

            encoded_image = self.image_reader.read(
                session=session, image_data=images[i], processing_fn=processing_fn)
            example = self.create_example(encoded_image, labels[i],
                                          filenames[i] if self.store_filenames else None)
            writer.write(example.SerializeToString())
