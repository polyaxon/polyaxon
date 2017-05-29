# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys
import tarfile

import tensorflow as tf

from six.moves import urllib
from tensorflow.python.framework.errors_impl import NotFoundError


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
        print()

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
            for i in range(3):
                details(img[i, :, :, :] if channels > 1 else img[i, :, :, 0], lab[i])

            coord.request_stop()
            coord.join(threads)
