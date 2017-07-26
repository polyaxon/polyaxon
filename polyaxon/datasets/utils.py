# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys
import tarfile

from six.moves import xrange

import tensorflow as tf

from six.moves import urllib
from tensorflow.python.framework.errors_impl import NotFoundError

from polyaxon import Modes
from polyaxon.libs.configs import PipelineConfig
from polyaxon.processing import create_input_data_fn


def make_dataset_dir(dataset_dir):
    if not tf.gfile.Exists(dataset_dir):
        tf.gfile.MakeDirs(dataset_dir)


def download_datasets(dataset_dir, url, filenames, uncompress=False):
    """Download datasets (uncompress) based on url + filenames locally.

    Args:
        dataset_dir: The directory where the temporary files are stored.
        url: `str`. The base url to download the data from
        filenames: `list`. list of filenames to download form the url.
        uncompress: `bool`. If set to `True`, uncompress the data
    """
    for filename in filenames:
        filepath = os.path.join(dataset_dir, filename)

        if os.path.exists(filepath):
            return

        print('Downloading file %s...' % filename)

        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %.1f%%' % (
                float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()

        filepath, _ = urllib.request.urlretrieve(url + filename, filepath, _progress)

        with tf.gfile.GFile(filepath) as f:
            size = f.size()
        print('Successfully downloaded', filename, size, 'bytes.')

        if uncompress:
            tarfile.open(filepath, 'r:gz').extractall(dataset_dir)


def delete_datasets(dataset_dir, filenames):
    """Removes temporary files used to create the dataset.

    Args:
        dataset_dir: `str`. The directory where the temporary files are stored.
        filenames: `list`. list of filenames to download form the url.
    """
    for filename in filenames:
        filepath = os.path.join(dataset_dir, filename)
        try:
            tf.gfile.Remove(filepath)
        except NotFoundError:
            pass


def count_tfrecord_file_content(tfrecord_filename):
    return len([_ for _ in tf.python_io.tf_record_iterator(tfrecord_filename)])


def verify_tfrecord_image(dataset_dir, create_input_fn, channels=3):
    import matplotlib.pyplot as plt
    from tensorflow.python.training import coordinator
    from tensorflow.python.training import queue_runner_impl

    def details(img, label):
        print('------image: {}'.format(label))
        plt.imshow(img)
        plt.show()

    create_input_fns = create_input_fn(dataset_dir)

    for input_fn in create_input_fns:
        with tf.Session() as session:
            image, label = input_fn()
            coord = coordinator.Coordinator()
            threads = queue_runner_impl.start_queue_runners(session, coord=coord)
            img, lab = session.run([image['image'], label['label']])

            print('Train data {}'.format(img[:, :, :].shape))
            for i in xrange(3):
                details(img[i, :, :, :] if channels > 1 else img[i, :, :, 0], lab[i])

            coord.request_stop()
            coord.join(threads)


def create_image_dataset_input_fn(dataset_dir, prepare_fn, record_file_name_format,
                                  meta_data_file_name_format):
    prepare_fn(dataset_dir)
    train_data_file = record_file_name_format.format(dataset_dir, Modes.TRAIN)
    eval_data_file = record_file_name_format.format(dataset_dir, Modes.EVAL)
    meta_data_filename = meta_data_file_name_format.format(dataset_dir)
    train_input_fn = create_input_data_fn(
        mode=Modes.TRAIN,
        pipeline_config=PipelineConfig(module='TFRecordImagePipeline', dynamic_pad=False,
                                       params={'data_files': train_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    eval_input_fn = create_input_data_fn(
        mode=Modes.EVAL,
        pipeline_config=PipelineConfig(module='TFRecordImagePipeline', dynamic_pad=False,
                                       params={'data_files': eval_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    return train_input_fn, eval_input_fn


def create_image_dataset_predict_input_fn(dataset_dir, prepare_fn, record_file_name_format,
                                          meta_data_file_name_format):
    prepare_fn(dataset_dir)
    test_data_file = record_file_name_format.format(dataset_dir, Modes.PREDICT)
    meta_data_filename = meta_data_file_name_format.format(dataset_dir)
    test_input_fn = create_input_data_fn(
        mode=Modes.PREDICT,
        pipeline_config=PipelineConfig(module='TFRecordImagePipeline', dynamic_pad=False,
                                       num_epochs=1,
                                       params={'data_files': test_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    return test_input_fn


def create_sequence_dataset_input_fn(dataset_dir, prepare_fn, record_file_name_format,
                                     meta_data_file_name_format, bucket_boundaries):
    prepare_fn(dataset_dir)
    train_data_file = record_file_name_format.format(dataset_dir, Modes.TRAIN)
    eval_data_file = record_file_name_format.format(dataset_dir, Modes.EVAL)
    meta_data_filename = meta_data_file_name_format.format(dataset_dir)
    train_input_fn = create_input_data_fn(
        mode=Modes.TRAIN,
        pipeline_config=PipelineConfig(module='TFRecordSequencePipeline', dynamic_pad=True,
                                       bucket_boundaries=bucket_boundaries,
                                       params={'data_files': train_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    eval_input_fn = create_input_data_fn(
        mode=Modes.EVAL,
        pipeline_config=PipelineConfig(module='TFRecordImagePipeline', dynamic_pad=True,
                                       bucket_boundaries=bucket_boundaries,
                                       params={'data_files': eval_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    return train_input_fn, eval_input_fn


def create_sequence_dataset_predict_input_fn(dataset_dir, prepare_fn, record_file_name_format,
                                             meta_data_file_name_format, bucket_boundaries):
    prepare_fn(dataset_dir)
    test_data_file = record_file_name_format.format(dataset_dir, Modes.PREDICT)
    meta_data_filename = meta_data_file_name_format.format(dataset_dir)
    test_input_fn = create_input_data_fn(
        mode=Modes.PREDICT,
        pipeline_config=PipelineConfig(module='TFRecordSequencePipeline', dynamic_pad=True,
                                       num_epochs=1, batch_size=4, min_after_dequeue=0,
                                       bucket_boundaries=bucket_boundaries,
                                       params={'data_files': test_data_file,
                                               'meta_data_file': meta_data_filename})
    )
    return test_input_fn
