# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pickle
import json
import sys

import numpy as np
import tensorflow as tf

from polyaxon import ModeKeys
from polyaxon.datasets.converters import ImagesToTFExampleConverter, PNGNumpyImageReader
from polyaxon.datasets.utils import download_datasets, make_dataset_dir, count_tfrecord_file_content

_DATA_URL = 'https://www.cs.toronto.edu/~kriz/'

_FILENAME = 'cifar-10-python.tar.gz'

_DATA_BATCH_FILENAME_FORMAT = '{}/cifar-10-batches-py/data_batch_{}'
_TEST_DATA_BATCH_FILENAME = '{}/cifar-10-batches-py/test_batch'

_NUM_CHANNELS = 3

_IMAGE_SIZE = 32

_IMAGE_FORMAT = 'png'

_IMAGE_COLORSPACE = 'RGB'

_FOLDS = 10

MEAT_DATA_FILENAME_FORMAT = '{}/meta_data.json'

RECORD_FILE_NAME_FORMAT = '{}/cifar_{}.tfrecord'


def _extract_data(filename):
    with tf.gfile.Open(filename, 'rb') as f:
        if sys.version_info > (3, 0):
            # Python3
            data = pickle.load(f, encoding='latin1')
        else:
            # Python2
            data = pickle.load(f)

    images = data['data']
    num_images = images.shape[0]

    images = images.reshape((num_images, 3, 32, 32))
    images = [np.squeeze(image).transpose((1, 2, 0)) for image in images]
    labels = data['labels']

    return labels, images


def prepare_dataset(converter, dataset_dir, data_name, filenames):
    filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, data_name)
    if tf.gfile.Exists(filename):
        print('`{}` Dataset files already exist. '
              'Exiting without re-creating them.'.format(filename))
        return

    with tf.python_io.TFRecordWriter(filename) as tfrecord_writer:
        with tf.Session('') as session:
            for filename in filenames:
                labels, images = _extract_data(filename)
                converter.convert(session=session, writer=tfrecord_writer, images=images,
                                  labels=labels, total_num_items=len(images))


def prepare(dataset_dir):
    """Runs download and conversion operation.

    Args:
        dataset_dir: The dataset directory where the dataset is stored.
    """
    make_dataset_dir(dataset_dir)

    download_datasets(dataset_dir, _DATA_URL, [_FILENAME], uncompress=True)

    image_reader = PNGNumpyImageReader(shape=(_IMAGE_SIZE, _IMAGE_SIZE, _NUM_CHANNELS))
    classes = [
        'airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'
    ]
    converter = ImagesToTFExampleConverter(
        classes=classes, colorspace=_IMAGE_COLORSPACE, image_format=_IMAGE_COLORSPACE,
        channels=_NUM_CHANNELS, image_reader=image_reader, height=_IMAGE_SIZE, width=_IMAGE_SIZE)

    prepare_dataset(converter, dataset_dir, ModeKeys.TRAIN,
                    [_DATA_BATCH_FILENAME_FORMAT.format(dataset_dir, i) for i in range(1, 5)])
    prepare_dataset(converter, dataset_dir, ModeKeys.EVAL,
                    [_DATA_BATCH_FILENAME_FORMAT.format(dataset_dir, 5)])
    prepare_dataset(converter, dataset_dir, 'test', [_TEST_DATA_BATCH_FILENAME.format(dataset_dir)])

    # Finally, write the meta data:
    with open(MEAT_DATA_FILENAME_FORMAT.format(dataset_dir), 'w') as meta_data_file:
        meta_data = converter.get_meta_data()
        meta_data['num_samples'] = {
            ModeKeys.TRAIN: count_tfrecord_file_content(
                RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.TRAIN)),
            ModeKeys.EVAL: count_tfrecord_file_content(
                RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.EVAL)),
            'test': count_tfrecord_file_content(
                RECORD_FILE_NAME_FORMAT.format(dataset_dir, 'test'))
        }
        meta_data['items_to_descriptions'] = {
            'image': 'A image of colorspace {} resized to {}.'.format(
                _IMAGE_COLORSPACE, _IMAGE_SIZE),
            'label': 'A single integer between 0 and {}'.format(len(classes)),
        }
        json.dump(meta_data, meta_data_file)

    print('\nFinished converting the flowers17 dataset!')


prepare('./cifar')
