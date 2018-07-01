from __future__ import absolute_import, division, print_function

import argparse

import tensorflow as tf
from polyaxon_helper import get_data_path
from tensorflow.examples.tutorials.mnist import input_data


data_paths = list(get_data_path().values())[0]
data_paths = "{}/mnist".format(data_paths)
print('Downloading data to {} ...'.format(data_paths))
input_data.read_data_sets(data_paths, one_hot=False)
print('Data downloaded ...')
