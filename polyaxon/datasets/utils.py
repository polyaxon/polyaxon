# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys
import tarfile

import tensorflow as tf

from six.moves import urllib


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
        tf.gfile.Remove(filepath)
