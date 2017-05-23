# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tempfile

import tensorflow as tf

from tensorflow.contrib.slim.python.slim import queues
from tensorflow.contrib.slim.python.slim.data import test_utils
from tensorflow.contrib import slim as tfslim
from tensorflow.python.client import session
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import image_ops
from tensorflow.python.platform import gfile
from tensorflow.python.platform import test

from polyaxon.processing.data_decoders import TFExampleDecoder
from polyaxon.processing.data_providers import Dataset, DatasetDataProvider


def _resize_image(image, height, width):
    image = array_ops.expand_dims(image, 0)
    image = image_ops.resize_bilinear(image, [height, width])
    return array_ops.squeeze(image, [0])


def _create_tfrecord_dataset(tmpdir):
    if not gfile.Exists(tmpdir):
        gfile.MakeDirs(tmpdir)

    data_sources = test_utils.create_tfrecord_files(tmpdir, num_files=1)

    keys_to_features = {
        'image/encoded': tf.FixedLenFeature(shape=(), dtype=dtypes.string, default_value=''),
        'image/format': tf.FixedLenFeature(shape=(), dtype=dtypes.string, default_value='jpeg'),
        'image/class/label': tf.FixedLenFeature(
            shape=[1], dtype=dtypes.int64,
            default_value=array_ops.zeros([1], dtype=dtypes.int64))
    }

    items_to_handlers = {
        'image': tfslim.tfexample_decoder.Image(),
        'label': tfslim.tfexample_decoder.Tensor('image/class/label'),
    }

    decoder = TFExampleDecoder(keys_to_features, items_to_handlers)

    return Dataset(
        data_sources=data_sources, reader=tf.TFRecordReader, decoder=decoder, num_samples=100)


class DatasetDataProviderTest(test.TestCase):
    def test_TFRecordDataset(self):
        dataset_dir = tempfile.mkdtemp(prefix=os.path.join(self.get_temp_dir(), 'tfrecord_dataset'))

        height = 300
        width = 280

        with self.test_session():
            test_dataset = _create_tfrecord_dataset(dataset_dir)
            provider = DatasetDataProvider(test_dataset)
            key, image, label = provider.get(['record_key', 'image', 'label'])
            image = _resize_image(image, height, width)

            with session.Session('') as sess:
                with queues.QueueRunners(sess):
                    key, image, label = sess.run([key, image, label])
            split_key = key.decode('utf-8').split(':')
            self.assertEqual(2, len(split_key))
            self.assertEqual(test_dataset.data_sources[0], split_key[0])
            self.assertTrue(split_key[1].isdigit())
            self.assertListEqual([height, width, 3], list(image.shape))
            self.assertListEqual([1], list(label.shape))

    def test_TFRecordSeparateGetDataset(self):
        dataset_dir = tempfile.mkdtemp(prefix=os.path.join(self.get_temp_dir(),
                                                           'tfrecord_separate_get'))

        height = 300
        width = 280

        with self.test_session():
            provider = DatasetDataProvider(_create_tfrecord_dataset(dataset_dir))

        [image] = provider.get(['image'])
        [label] = provider.get(['label'])
        image = _resize_image(image, height, width)

        with session.Session('') as sess:
            with queues.QueueRunners(sess):
                image, label = sess.run([image, label])
            self.assertListEqual([height, width, 3], list(image.shape))
            self.assertListEqual([1], list(label.shape))

    def test_conflicting_record_key_item(self):
        dataset_dir = tempfile.mkdtemp(prefix=os.path.join(self.get_temp_dir(), 'tfrecord_dataset'))

        with self.test_session():
            with self.assertRaises(ValueError):
                DatasetDataProvider(_create_tfrecord_dataset(dataset_dir), record_key='image')


if __name__ == '__main__':
    test.main()
