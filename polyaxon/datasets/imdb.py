# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

import six.moves.cPickle as pickle

import numpy as np
import tensorflow as tf

from polyaxon import Modes
from polyaxon.datasets.converters.sequence_converters import SequenceToTFExampleConverter
from polyaxon.datasets.utils import (
    download_datasets,
    delete_datasets,
    make_dataset_dir,
    create_sequence_dataset_input_fn,
    create_sequence_dataset_predict_input_fn
)

_DATA_URL = 'http://www.iro.umontreal.ca/~lisa/deep/data/'
_FILENAME = 'imdb.pkl'
_MAX_TOKEN = 10000
_UNK = 1

META_DATA_FILENAME_FORMAT = '{}/meta_data.json'

RECORD_FILE_NAME_FORMAT = '{}/imdb_{}.tfrecord'


def _clean_tokens(seq):
    return [1 if t >= _MAX_TOKEN else t for t in seq]


def prepare_dataset(converter, dataset_dir, dataset, data_name, num_items, num_eval=0):
    filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, data_name)
    if num_eval:
        eval_filename = RECORD_FILE_NAME_FORMAT.format(dataset_dir, Modes.EVAL)

    if tf.gfile.Exists(filename):
        print('`{}` Dataset files already exist. '
              'Exiting without re-creating them.'.format(filename))
        return

    tokens = dataset[0]
    labels = dataset[1]
    if num_eval:
        # split data
        idx = np.random.permutation(num_items)
        eval_tokens = [{'source_token': _clean_tokens(tokens[i])} for i in idx[:num_eval]]
        eval_labels = [{'label': labels[i]} for i in idx[:num_eval]]
        tokens = [{'source_token': _clean_tokens(tokens[i])} for i in idx[num_eval:]]
        labels = [{'label': labels[i]} for i in idx[num_eval:]]
    else:
        tokens = [{'source_token': _clean_tokens(t)} for t in tokens[:100]]
        labels = [{'label': l} for l in labels]

    with tf.python_io.TFRecordWriter(filename) as tfrecord_writer:
        with tf.Session('') as session:
            converter.convert(session=session, writer=tfrecord_writer,
                              sequence_features_list=tokens,
                              context_features_list=labels,
                              total_num_items=num_items - num_eval)

    if num_eval:
        with tf.python_io.TFRecordWriter(eval_filename) as tfrecord_writer:
            with tf.Session('') as session:
                converter.convert(session=session, writer=tfrecord_writer,
                                  sequence_features_list=eval_tokens,
                                  context_features_list=eval_labels,
                                  total_num_items=num_eval)


def prepare(dataset_dir):
    """Runs download and conversion operation.

    Args:
        dataset_dir: The dataset directory where the dataset is stored.
    """
    make_dataset_dir(dataset_dir)
    if all([
        tf.gfile.Exists(RECORD_FILE_NAME_FORMAT.format(dataset_dir, Modes.TRAIN)),
        tf.gfile.Exists(RECORD_FILE_NAME_FORMAT.format(dataset_dir, Modes.EVAL)),
        tf.gfile.Exists(RECORD_FILE_NAME_FORMAT.format(dataset_dir, Modes.PREDICT)),
    ]):
        print('`{}` Dataset files already exist.')
        return

    download_datasets(dataset_dir, _DATA_URL, [_FILENAME])
    with open(os.path.join(dataset_dir, _FILENAME), 'rb') as f:
        train_set = pickle.load(f)
        test_set = pickle.load(f)

    converter = SequenceToTFExampleConverter(sequence_features_types={'source_token': 'int'},
                                             context_features_types={'label': 'int'})

    num_items = len(train_set[0])
    len_eval_data = int(num_items * 0.1)
    len_test_data = len(test_set[0])
    prepare_dataset(converter, dataset_dir, train_set, Modes.TRAIN, num_items, len_eval_data)
    prepare_dataset(converter, dataset_dir, test_set, Modes.PREDICT, len_test_data)

    # Finally, write the meta data:
    with open(META_DATA_FILENAME_FORMAT.format(dataset_dir), 'w') as meta_data_file:
        meta_data = converter.get_meta_data()
        meta_data['num_samples'] = {Modes.TRAIN: num_items - len_eval_data,
                                    Modes.EVAL: len_eval_data,
                                    Modes.PREDICT: len_test_data}
        meta_data['items_to_descriptions'] = {
            'source_token': 'A sequence of word ids.',
            'label': 'A single integer 0 or 1',
        }
        meta_data['num_classes'] = 2
        json.dump(meta_data, meta_data_file)

    delete_datasets(dataset_dir, [_FILENAME])
    print('\nFinished converting the IMDB dataset!')


def create_input_fn(dataset_dir):
    return create_sequence_dataset_input_fn(
        dataset_dir, prepare, RECORD_FILE_NAME_FORMAT, META_DATA_FILENAME_FORMAT,
        bucket_boundaries=[140, 200, 300, 400, 500])


def create_predict_input_fn(dataset_dir):
    return create_sequence_dataset_predict_input_fn(
        dataset_dir, prepare, RECORD_FILE_NAME_FORMAT, META_DATA_FILENAME_FORMAT,
        bucket_boundaries=[140, 200, 300, 400, 500])

