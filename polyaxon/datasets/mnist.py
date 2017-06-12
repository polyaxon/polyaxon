# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import gzip
import json
import os

import numpy as np
import tensorflow as tf

from polyaxon import ModeKeys
from polyaxon.datasets.converters import ImagesToTFExampleConverter, PNGNumpyImageReader
from polyaxon.datasets.utils import (
    download_datasets,
    delete_datasets,
    make_dataset_dir,
    create_dataset_input_fn,
    create_dataset_test_input_fn
)

_DATA_URL = 'http://yann.lecun.com/exdb/mnist/'
_TRAIN_DATA_FILENAME = 'train-images-idx3-ubyte.gz'
_TRAIN_LABELS_FILENAME = 'train-labels-idx1-ubyte.gz'
_TEST_DATA_FILENAME = 't10k-images-idx3-ubyte.gz'
_TEST_LABELS_FILENAME = 't10k-labels-idx1-ubyte.gz'

MEAT_DATA_FILENAME_FORMAT = '{}/meta_data.json'

RECORD_FILE_NAME_FORMAT = '{}/mnist_{}.tfrecord'

_IMAGE_SIZE = 28
_NUM_CHANNELS = 1


def _extract_images(filename, num_images):
    """Extract the images into a numpy array.

    Args:
        filename: The path to an MNIST images file.
        num_images: The number of images in the file.

    Returns:
        A numpy array of shape [number_of_images, height, width, channels].
    """
    print('Extracting images from: ', filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(16)
        buf = bytestream.read(_IMAGE_SIZE * _IMAGE_SIZE * num_images * _NUM_CHANNELS)
        data = np.frombuffer(buf, dtype=np.uint8)
        data = data.reshape(num_images, _IMAGE_SIZE, _IMAGE_SIZE, _NUM_CHANNELS)
    return data


def _extract_labels(filename, num_labels):
    """Extract the labels into a vector of int64 label IDs.

    Args:
        filename: The path to an MNIST labels file.
        num_labels: The number of labels in the file.

    Returns:
        A numpy array of shape [number_of_labels]
    """
    print('Extracting labels from: ', filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(8)
        buf = bytestream.read(1 * num_labels)
        labels = np.frombuffer(buf, dtype=np.uint8).astype(np.int64)
    return labels


def prepare_dataset(converter, dataset_dir, data_name, num_images, num_eval=0):
    filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, data_name)
    if num_eval:
        eval_filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.EVAL)

    if tf.gfile.Exists(filename):
        print('`{}` Dataset files already exist. '
              'Exiting without re-creating them.'.format(filename))
        return

    if data_name == ModeKeys.TRAIN:
        filenames = [_TRAIN_DATA_FILENAME, _TRAIN_LABELS_FILENAME]
    else:
        filenames = [_TEST_DATA_FILENAME, _TEST_LABELS_FILENAME]

    download_datasets(dataset_dir, _DATA_URL, filenames)

    if data_name == ModeKeys.TRAIN:
        data_filename = os.path.join(dataset_dir, _TRAIN_DATA_FILENAME)
        labels_filename = os.path.join(dataset_dir, _TRAIN_LABELS_FILENAME)
    else:
        data_filename = os.path.join(dataset_dir, _TEST_DATA_FILENAME)
        labels_filename = os.path.join(dataset_dir, _TEST_LABELS_FILENAME)

    images = _extract_images(data_filename, num_images)
    labels = _extract_labels(labels_filename, num_images)
    if num_eval:
        images, eval_images = images[num_eval:], images[:num_eval]
        labels, eval_labels = labels[num_eval:], labels[:num_eval]

    with tf.python_io.TFRecordWriter(filename) as tfrecord_writer:
        with tf.Session('') as session:
            converter.convert(session=session, writer=tfrecord_writer, images=images,
                              labels=labels, total_num_items=len(images))

    if num_eval:
        with tf.python_io.TFRecordWriter(eval_filename) as tfrecord_writer:
            with tf.Session('') as session:
                converter.convert(session=session, writer=tfrecord_writer, images=eval_images,
                                  labels=eval_labels, total_num_items=len(eval_images))

    delete_datasets(dataset_dir, filenames)


def prepare(dataset_dir):
    """Runs download and conversion operation.

    Args:
        dataset_dir: The dataset directory where the dataset is stored.
    """
    make_dataset_dir(dataset_dir)

    image_reader = PNGNumpyImageReader(shape=(_IMAGE_SIZE, _IMAGE_SIZE, _NUM_CHANNELS))
    classes = ['zero', 'one', 'two', 'three', 'four', 'five', 'size', 'seven', 'eight', 'nine']
    converter = ImagesToTFExampleConverter(
        classes=classes, colorspace='grayscale', image_format='png',
        channels=_NUM_CHANNELS, image_reader=image_reader, height=_IMAGE_SIZE, width=_IMAGE_SIZE)

    prepare_dataset(converter, dataset_dir, ModeKeys.TRAIN, 60000, num_eval=10000)
    prepare_dataset(converter, dataset_dir, 'test', 10000)

    # Finally, write the meta data:
    with open(MEAT_DATA_FILENAME_FORMAT.format(dataset_dir), 'w') as meta_data_file:
        meta_data = converter.get_meta_data()
        meta_data['num_samples'] = {ModeKeys.TRAIN: 50000,
                                    ModeKeys.EVAL: 10000,
                                    ModeKeys.PREDICT: 10000}
        meta_data['items_to_descriptions'] = {
            'image': 'A image of fixed size 28.',
            'label': 'A single integer between 0 and 9',
        }
        json.dump(meta_data, meta_data_file)

    print('\nFinished converting the MNIST dataset!')


def create_input_fn(dataset_dir):
    return create_dataset_input_fn(
        dataset_dir, prepare, RECORD_FILE_NAME_FORMAT, MEAT_DATA_FILENAME_FORMAT)


def create_test_input_fn(dataset_dir):
    return create_dataset_test_input_fn(
        dataset_dir, prepare, RECORD_FILE_NAME_FORMAT, MEAT_DATA_FILENAME_FORMAT)

