# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
from collections import defaultdict
from random import shuffle

import tensorflow as tf

from polyaxon import ModeKeys
from polyaxon.datasets.converters import (
    ImagesToTFExampleConverter,
    JPEGImageReader,
    JPGNumpyImageReader
)
from polyaxon.datasets.utils import download_datasets, delete_datasets, make_dataset_dir
from polyaxon.libs.configs import PipelineConfig
from polyaxon.processing import create_input_data_fn
from polyaxon.processing.image import resize

_DATA_URL = 'http://www.robots.ox.ac.uk/~vgg/data/flowers/17/'

_FILENAME = '17flowers.tgz'

_NUM_CHANNELS = 3

_IMAGE_SIZE = 224

_IMAGE_FORMAT = 'jpeg'

_IMAGE_COLORSPACE = 'RGB'

_FOLDS = 10

MEAT_DATA_FILENAME_FORMAT = '{}/meta_data.json'

RECORD_FILE_NAME_FORMAT = '{}/flowers_{}.tfrecord'


def filenames_by_classes(dataset_dir, num_images, folds):
    class_id = 0
    filenames_classes = defaultdict(list)
    for i in range(1, num_images + 1):
        fname = 'image_{:04d}.jpg'.format(i)
        filenames_classes[class_id].append('{}/jpg/{}'.format(dataset_dir, fname))
        if i % 80 == 0 and class_id < 16:
            class_id += 1

    train_filenames_by_classes = {}
    eval_filenames_by_classes = {}
    test_filenames_by_classes = {}

    for i in range(17):
        shuffle(filenames_classes[i])
        parts = len(filenames_classes[i]) // folds
        train_filenames_by_classes[i] = filenames_classes[i][2 * parts:]
        eval_filenames_by_classes[i] = filenames_classes[i][:parts]
        test_filenames_by_classes[i] = filenames_classes[i][parts:2 * parts]
    return {ModeKeys.TRAIN: train_filenames_by_classes,
            ModeKeys.EVAL: eval_filenames_by_classes,
            'test': test_filenames_by_classes}


def convert_images(session, writer, converter, filesnames_by_classes):
    images = []
    labels = []
    image_filenames = []
    for class_id in filesnames_by_classes:
        for image_filename in filesnames_by_classes[class_id]:
            images.append(tf.gfile.FastGFile(image_filename, 'rb').read())
            labels.append(class_id)
            image_filenames.append(image_filename)

    image_encoder = JPGNumpyImageReader(shape=(_IMAGE_SIZE, _IMAGE_SIZE, _NUM_CHANNELS))

    def processing_fn(session, image):
        image = resize(image, _IMAGE_SIZE, _IMAGE_SIZE)
        image.set_shape((_IMAGE_SIZE, _IMAGE_SIZE, _NUM_CHANNELS))
        return image

    converter.convert(session=session, writer=writer, images=images, labels=labels,
                      total_num_items=len(images), filenames=image_filenames,
                      processing_fn=processing_fn, post_processing_fn=image_encoder.read)


def prepare_dataset(converter, dataset_dir, num_images, folds):
    train_filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.TRAIN)
    eval_filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.EVAL)
    test_filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, 'test')

    filenames = [train_filename, eval_filename, test_filename]
    files_exist = [tf.gfile.Exists(f) for f in filenames]
    if all(files_exist):
        print('Dataset files already exist. Exiting without re-creating them.')
        return

    if any(files_exist):
        print('Some Dataset files already exist but not all of them. Re-creating them.')
        delete_datasets('.', filenames)

    filesnames_by_classes = filenames_by_classes(dataset_dir, num_images, folds)

    with tf.python_io.TFRecordWriter(train_filename) as tfrecord_writer:
        with tf.Session('') as session:
            print('converting {} images.'.format(ModeKeys.TRAIN))
            convert_images(
                session, tfrecord_writer, converter, filesnames_by_classes[ModeKeys.TRAIN])

    with tf.python_io.TFRecordWriter(eval_filename) as tfrecord_writer:
        with tf.Session('') as session:
            print('converting {} images.'.format(ModeKeys.EVAL))
            convert_images(
                session, tfrecord_writer, converter, filesnames_by_classes[ModeKeys.EVAL])

    with tf.python_io.TFRecordWriter(test_filename) as tfrecord_writer:
        with tf.Session('') as session:
            print('converting test images.')
            convert_images(session, tfrecord_writer, converter, filesnames_by_classes['test'])


def prepare(dataset_dir):
    """Runs download and conversion operation.

    Args:
        dataset_dir: The dataset directory where the dataset is stored.
    """
    make_dataset_dir(dataset_dir)

    download_datasets(dataset_dir, _DATA_URL, [_FILENAME], uncompress=True)

    image_reader = JPEGImageReader(channels=_NUM_CHANNELS)
    converter = ImagesToTFExampleConverter(
        classes=list(range(17)), colorspace=_IMAGE_COLORSPACE, image_format=_IMAGE_FORMAT,
        channels=_NUM_CHANNELS, image_reader=image_reader, height=_IMAGE_SIZE, width=_IMAGE_SIZE)

    prepare_dataset(converter, dataset_dir, 1360, folds=_FOLDS)

    # Finally, write the meta data:
    with open(MEAT_DATA_FILENAME_FORMAT.format(dataset_dir), 'w') as meta_data_file:
        meta_data = converter.get_meta_data()
        meta_data['num_samples'] = {ModeKeys.TRAIN: 1360 - 2 * (1360 // _FOLDS),
                                    ModeKeys.EVAL: 1360 // _FOLDS,
                                    'test': 1360 // _FOLDS}
        meta_data['items_to_descriptions'] = {
            'image': 'A image of colorspace {} resized to {}.'.format(
                _IMAGE_COLORSPACE, _IMAGE_SIZE),
            'label': 'A single integer between 0 and 16',
        }
        json.dump(meta_data, meta_data_file)

    print('\nFinished converting the flowers17 dataset!')


def create_input_fn(dataset_dir):
    prepare(dataset_dir)
    train_data_file = RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.TRAIN)
    eval_data_file = RECORD_FILE_NAME_FORMAT.format(dataset_dir, ModeKeys.EVAL)
    meta_data_filename = MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)
    train_input_fn = create_input_data_fn(
        mode=ModeKeys.TRAIN,
        pipeline_config=PipelineConfig(name='TFRecordImagePipeline', dynamic_pad=False,
                                       params={'data_files': train_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    eval_input_fn = create_input_data_fn(
        mode=ModeKeys.EVAL,
        pipeline_config=PipelineConfig(name='TFRecordImagePipeline', dynamic_pad=False,
                                       params={'data_files': eval_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    return train_input_fn, eval_input_fn
