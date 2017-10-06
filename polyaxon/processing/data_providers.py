# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
# pylint:  disable=too-many-lines

import abc
import six

import numpy as np
import tensorflow as tf

from tensorflow.contrib.slim.python.slim.data.parallel_reader import parallel_read


class Dataset(object):
    """Represents a Dataset specification.

    Args:
        data_sources: A list of files that make up the dataset.
        reader: The reader class, a subclass of BaseReader, e.g. TFRecordReader.
        decoder: An instance of a data_decoder.
        num_samples: The number of samples in the dataset.
        items_to_descriptions: A map from the items that the dataset provides to
            the descriptions of those items.
        meta_data: extra information about the current dataset, e.g. num_samples, channels ...
            Generally read from the meta_data.json file
        **kwargs: Any remaining dataset-specific fields.
    """

    def __init__(self, data_sources, reader, decoder, num_samples=None, items_to_descriptions=None,
                 meta_data=None, **kwargs):
        kwargs['data_sources'] = data_sources
        kwargs['reader'] = reader
        kwargs['decoder'] = decoder
        kwargs['num_samples'] = num_samples
        kwargs['items_to_descriptions'] = items_to_descriptions or {}
        kwargs['meta_data'] = meta_data or {}
        self.__dict__.update(kwargs)


@six.add_metaclass(abc.ABCMeta)
class DataProvider(object):
    """Maps a list of requested data items to tensors from a data source.
    (A mirror to tf.slim.data DataProvider)

    All data providers must inherit from DataProvider and implement the Get
    method which returns arbitrary types of data. No assumption is made about the
    source of the data nor the mechanism for providing it.

    Args:
        items_to_tensors: a dictionary of names to tensors.
        num_samples: the number of samples in the dataset being provided.
    """
    def __init__(self, items_to_tensors, num_samples):
        self._items_to_tensors = items_to_tensors
        self._num_samples = num_samples

    def get(self, items):
        """Returns a list of tensors specified by the given list of items.

        The list of items is arbitrary different data providers satisfy different
        lists of items. For example the Pascal VOC might accept items 'image' and
        'semantics', whereas the NYUDepthV2 data provider might accept items
        'image', 'depths' and 'normals'.

        Args:
            items: a list of strings, each of which indicate a particular data type.

        Returns:
            a list of tensors, whose length matches the length of `items`, where each
            tensor corresponds to each item.

        Raises:
            ValueError: if any of the items cannot be satisfied.
        """
        self._validate_items(items)
        return [self._items_to_tensors[item] for item in items]

    def list_items(self):
        """Returns the list of item names that can be provided by the data provider.

        Returns:
            a list of item names that can be passed to Get([items]).
        """
        return self._items_to_tensors.keys()

    def num_samples(self):
        """Returns the number of data samples in the dataset.

        Returns:
            a positive whole number.
        """
        return self._num_samples

    def _validate_items(self, items):
        """Verifies that each given item is a member of the list from ListItems().

        Args:
            items: a list or tuple of strings.

        Raises:
            ValueError: if `items` is not a tuple or list or if any of the elements of
                `items` is not found in the list provided by self.ListItems().
        """
        if not isinstance(items, (list, tuple)):
            raise ValueError('items must be a list or tuple')

        valid_items = self.list_items()
        for item in items:
            if item not in valid_items:
                raise ValueError('Item [{}] is invalid. Valid entries include: {}'.format(
                    item, valid_items))


class DatasetDataProvider(DataProvider):
    """Creates a DatasetDataProvider.

    Args:
        dataset: An instance of the Dataset class.
        num_readers: The number of parallel readers to use.
        reader_kwargs: An optional dict of kwargs for the reader.
        shuffle: Whether to shuffle the data sources and common queue when reading.
        num_epochs: The number of times each data source is read. If left as None,
            the data will be cycled through indefinitely.
        common_queue_capacity: The capacity of the common queue.
        common_queue_min: The minimum number of elements in the common queue after a dequeue.
        record_key: The item name to use for the dataset record keys in the provided tensors.
        seed: The seed to use if shuffling.
        scope: Optional name scope for the ops.
    Raises:
        ValueError: If `record_key` matches one of the items in the dataset.
    """
    def __init__(self, dataset, num_readers=1, reader_kwargs=None, shuffle=True, num_epochs=None,
                 common_queue_capacity=256, common_queue_min=128, record_key='__record_key__',
                 seed=None, scope=None):
        _, data = parallel_read(
            dataset.data_sources,
            reader_class=dataset.reader,
            num_epochs=num_epochs,
            num_readers=num_readers,
            reader_kwargs=reader_kwargs,
            shuffle=shuffle,
            capacity=common_queue_capacity,
            min_after_dequeue=common_queue_min,
            seed=seed,
            scope=scope)

        items = dataset.decoder.list_items()
        tensors = dataset.decoder.decode(data, items)

        if record_key in items:
            raise ValueError('The item name used for `record_key` cannot also be '
                             'used for a dataset item: %s', record_key)
        # items.append(record_key)
        # tensors.append(key)

        super(DatasetDataProvider, self).__init__(items_to_tensors=dict(zip(items, tensors)),
                                                  num_samples=dataset.num_samples)


class ParallelDatasetProvider(DataProvider):
    """Creates a ParallelDatasetProvider. This data provider reads two datasets
    in parallel, keeping them aligned.

    Args:
        dataset_source: The first dataset. An instance of the Dataset class.
        dataset_target: The second dataset. An instance of the Dataset class.
            Can be None. If None, only `dataset1` is read.
        shuffle: Whether to shuffle the data sources and common queue when
          reading.
        num_epochs: The number of times each data source is read. If left as None,
          the data will be cycled through indefinitely.
        common_queue_capacity: The capacity of the common queue.
        common_queue_min: The minimum number of elements in the common queue after a dequeue.
        seed: The seed to use if shuffling.
    """
    def __init__(self, dataset_source, dataset_target, shuffle=True, num_epochs=None,
                 common_queue_capacity=4096, common_queue_min=1024, seed=None):

        if seed is None:
            seed = np.random.randint(10e8)

        _, data_source = parallel_read(
            dataset_source.data_sources,
            reader_class=dataset_source.reader,
            num_epochs=num_epochs,
            num_readers=1,
            shuffle=False,
            capacity=common_queue_capacity,
            min_after_dequeue=common_queue_min,
            seed=seed)

        data_target = ""
        if dataset_target is not None:
            _, data_target = parallel_read(
                dataset_target.data_sources,
                reader_class=dataset_target.reader,
                num_epochs=num_epochs,
                num_readers=1,
                shuffle=False,
                capacity=common_queue_capacity,
                min_after_dequeue=common_queue_min,
                seed=seed)

        # Optionally shuffle the data
        if shuffle:
            shuffle_queue = tf.RandomShuffleQueue(
                capacity=common_queue_capacity,
                min_after_dequeue=common_queue_min,
                dtypes=[tf.string, tf.string],
                seed=seed)
            enqueue_ops = [shuffle_queue.enqueue([data_source, data_target])]
            tf.train.add_queue_runner(
                tf.train.QueueRunner(shuffle_queue, enqueue_ops))
            data_source, data_target = shuffle_queue.dequeue()

        # Decode source items
        items = dataset_source.decoder.list_items()
        tensors = dataset_source.decoder.decode(data_source, items)

        if dataset_target is not None:
            # Decode target items
            items2 = dataset_target.decoder.list_items()
            tensors2 = dataset_target.decoder.decode(data_target, items2)

            # Merge items and results
            items = items + items2
            tensors = tensors + tensors2

        super(ParallelDatasetProvider, self).__init__(items_to_tensors=dict(zip(items, tensors)),
                                                      num_samples=dataset_source.num_samples)


def make_parallel_data_provider(data_sources_source,
                                data_sources_target,
                                reader=tf.TextLineReader,
                                num_samples=None,
                                decoder_source=None,
                                decoder_target=None,
                                **kwargs):
    """Creates a DataProvider that reads parallel text data.

        Args:
            data_sources_source: A list of data sources for the source text files.
            data_sources_target: A list of data sources for the target text files.
              Can be None for inference mode.
            reader: ex: tf.TFRecordReader
            num_samples: Optional, number of records in the dataset
            delimiter: Split tokens in the data on this delimiter. Defaults to space.
            decoder_source: an instance of DataDecoder
            e.g.:
            ```python
            >>> decoder_source = SplitTokensDecoder(
            >>>     tokens_feature_name="source_token",
            >>>     length_feature_name="source_len",
            >>>     append_token="SEQUENCE_END",
            >>>     delimiter=" ")
            ```
            decoder_target: an instance of DataDecoder
            e.g.:
            ```python
            >>> decoder_target = SplitTokensDecoder(
            >>>     tokens_feature_name="target_token",
            >>>     length_feature_name="target_len",
            >>>     prepend_token="SEQUENCE_START",
            >>>     append_token="SEQUENCE_END",
            >>>     delimiter=target_delimiter)
            ```
            kwargs: Additional arguments (shuffle, num_epochs, etc) that are passed
              to the data provider

        Returns:
            A DataProvider instance
    """
    dataset_source = Dataset(
        data_sources=data_sources_source,
        reader=reader,
        decoder=decoder_source,
        num_samples=num_samples,
        items_to_descriptions={})

    dataset_target = None
    if data_sources_target is not None:
        dataset_target = Dataset(
            data_sources=data_sources_target,
            reader=reader,
            decoder=decoder_target,
            num_samples=num_samples,
            items_to_descriptions={})

    return ParallelDatasetProvider(
        dataset_source=dataset_source, dataset_target=dataset_target, **kwargs)
