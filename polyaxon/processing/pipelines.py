# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.contrib.slim.python.slim.data import tfexample_decoder

from polyaxon.experiments.subgraph import SubGraph
from polyaxon.processing.data_decoders import SplitTokensDecoder, TFSEquenceExampleDecoder
from polyaxon.processing.data_providers import ParallelDataProvider


class Pipeline(SubGraph):
    """Abstract InputPipeline class. All input pipelines must inherit from this.
    An InputPipeline defines how data is read, parsed, and separated into
    features and labels.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`, name to give for this pipeline.
        methods: `list`, list of methods to call in order to create this pipeline.
        kwargs: `list`, list of kwargs to use with the methods.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
    """

    def __init__(self, mode, name, methods=None, kwargs=None, shuffle=True, num_epochs=None):
        self.shuffle = shuffle
        self.num_epochs = num_epochs
        super(Pipeline, self).__init__(mode=mode, name=name, methods=methods, kwargs=kwargs)

    def make_data_provider(self, **kwargs):
        """Creates DataProvider instance for this input pipeline. Additional
        keyword arguments are passed to the DataProvider.
        """
        raise NotImplementedError("Not implemented.")

    @property
    def feature_keys(self):
        """Defines the features that this input pipeline provides. Returns
          a set of strings.
        """
        return set()

    @property
    def label_keys(self):
        """Defines the labels that this input pipeline provides. Returns
          a set of strings.
        """
        return set()

    @staticmethod
    def read_from_data_provider(data_provider):
        """Utility function to read all available items from a DataProvider."""
        item_values = data_provider.get(list(data_provider.list_items()))
        items_dict = dict(zip(data_provider.list_items(), item_values))
        return items_dict


class ParallelTextPipeline(Pipeline):
    """An input pipeline that reads two parallel (line-by-line aligned) text files.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`, name to give for this pipeline.
        methods: `list`, list of methods to call in order to create this pipeline.
        kwargs: `list`, list of kwargs to use with the methods.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
        source_files: An array of file names for the source data.
        target_files: An array of file names for the target data. These must
          be aligned to the `source_files`.
        source_delimiter: A character to split the source text on. Defaults
          to  " " (space). For character-level training this can be set to the
          empty string.
        target_delimiter: Same as `source_delimiter` but for the target text.
    """
    def __init__(self, mode, name, methods=None, kwargs=None, shuffle=True, num_epochs=None,
                 source_files=None, target_files=None, source_delimiter="", target_delimiter=""):
        self.source_files = source_files or []
        self.target_files = target_files or []
        self.source_delimiter = source_delimiter
        self.target_delimiter = target_delimiter
        super(ParallelTextPipeline, self).__init__(
            mode=mode, name=name, methods=methods, kwargs=kwargs,
            shuffle=shuffle, num_epochs=num_epochs)

    def make_data_provider(self, **kwargs):
        decoder_source = SplitTokensDecoder(
            tokens_feature_name='source_tokens',
            length_feature_name='source_len',
            append_token='SEQUENCE_END',
            delimiter=self.source_delimiter)

        dataset_source = tf.contrib.slim.dataset.Dataset(
            data_sources=self.source_files,
            reader=tf.TextLineReader,
            decoder=decoder_source,
            num_samples=None,
            items_to_descriptions={})

        dataset_target = None
        if len(self.target_files) > 0:
            decoder_target = SplitTokensDecoder(
                tokens_feature_name='target_tokens',
                length_feature_name='target_len',
                prepend_token='SEQUENCE_START',
                append_token='SEQUENCE_END',
                delimiter=self.target_delimiter)

            dataset_target = tf.contrib.slim.dataset.Dataset(
                data_sources=self.target_files,
                reader=tf.TextLineReader,
                decoder=decoder_target,
                num_samples=None,
                items_to_descriptions={})

        return ParallelDataProvider(
            dataset_source=dataset_source,
            dataset_target=dataset_target,
            shuffle=self.shuffle,
            num_epochs=self.num_epochs,
            **kwargs)

    @property
    def feature_keys(self):
        return {'source_tokens', 'source_len'}

    @property
    def label_keys(self):
        return {'target_tokens', 'target_len'}


class TFRecordPipeline(Pipeline):
    """An input pipeline that reads a TFRecords containing both source and target sequences.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`, name to give for this pipeline.
        methods: `list`, list of methods to call in order to create this pipeline.
        kwargs: `list`, list of kwargs to use with the methods.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
        files: An array of file names to read from.
        source_field: The TFRecord feature field containing the source text.
        target_field: The TFRecord feature field containing the target text.
        source_delimiter: A character to split the source text on. Defaults
          to  " " (space). For character-level training this can be set to the
          empty string.
        target_delimiter: Same as `source_delimiter` but for the target text.
    """

    def __init__(self, mode, name, methods=None, kwargs=None, shuffle=True, num_epochs=None,
                 files=None, source_field='source', target_field='target',
                 source_delimiter="", target_delimiter=""):
        self.files = files or []
        self.source_field = source_field
        self.target_field = target_field
        self.source_delimiter = source_delimiter
        self.target_delimiter = target_delimiter
        super(TFRecordPipeline, self).__init__(mode=mode, name=name, methods=methods, kwargs=kwargs,
                                               shuffle=shuffle, num_epochs=num_epochs)

    def make_data_provider(self, **kwargs):
        splitter_source = SplitTokensDecoder(
            tokens_feature_name='source_tokens',
            length_feature_name='source_len',
            append_token='SEQUENCE_END',
            delimiter=self.source_delimiter)

        splitter_target = SplitTokensDecoder(
            tokens_feature_name='target_tokens',
            length_feature_name='target_len',
            prepend_token='SEQUENCE_START',
            append_token='SEQUENCE_END',
            delimiter=self.target_delimiter)

        keys_to_features = {
            self.source_field: tf.FixedLenFeature((), tf.string),
            self.target_field: tf.FixedLenFeature(
                (), tf.string, default_value="")
        }

        items_to_handlers = {}
        items_to_handlers['source_tokens'] = tfexample_decoder.ItemHandlerCallback(
            keys=[self.source_field],
            func=lambda dict: splitter_source.decode(
                dict[self.source_field], ['source_tokens'])[0])
        items_to_handlers['source_len'] = tfexample_decoder.ItemHandlerCallback(
            keys=[self.source_field],
            func=lambda dict: splitter_source.decode(
                dict[self.source_field], ['source_len'])[0])
        items_to_handlers['target_tokens'] = tfexample_decoder.ItemHandlerCallback(
            keys=[self.target_field],
            func=lambda dict: splitter_target.decode(
                dict[self.target_field], ['target_tokens'])[0])
        items_to_handlers['target_len'] = tfexample_decoder.ItemHandlerCallback(
            keys=[self.target_field],
            func=lambda dict: splitter_target.decode(
                dict[self.target_field], ['target_len'])[0])

        decoder = tfexample_decoder.TFExampleDecoder(keys_to_features, items_to_handlers)

        dataset = tf.contrib.slim.dataset.Dataset(
            data_sources=self.files,
            reader=tf.TFRecordReader,
            decoder=decoder,
            num_samples=None,
            items_to_descriptions={})

        return tf.contrib.slim.dataset_data_provider.DatasetDataProvider(
            dataset=dataset,
            shuffle=self.shuffle,
            num_epochs=self.num_epochs,
            **kwargs)

    @property
    def feature_keys(self):
        return {'source_tokens', 'source_len'}

    @property
    def label_keys(self):
        return {'target_tokens', 'target_len'}


class ImageCaptioningPipeline(Pipeline):
    """An input pipeline that reads a TFRecords containing both source and target sequences.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`, name to give for this pipeline.
        methods: `list`, list of methods to call in order to create this pipeline.
        kwargs: `list`, list of kwargs to use with the methods.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
        files: An array of file names to read from.
        image_field: The TFRecord feature field containing the source images.
        image_format: The images extensions.
        caption_ids_field: The caption ids field.
        caption_tokens_field: the caption tokends field.
    """

    def __init__(self, mode, name,  methods=None, kwargs=None, shuffle=True, num_epochs=None,
                 files=None, image_field="image/data", image_format='jpg',
                 caption_ids_field="image/caption_ids", caption_tokens_field="image/caption"):
        self.files = files or []
        self.image_field = image_field
        self.image_format = image_format
        self.caption_ids_field = caption_ids_field
        self.caption_tokens_field = caption_tokens_field
        super(TFRecordPipeline).__init__(mode=mode, name=name, methods=methods, kwargs=kwargs,
                                         shuffle=shuffle, num_epochs=num_epochs)

    def make_data_provider(self, **kwargs):
        context_keys_to_features = {
            self.image_field: tf.FixedLenFeature(
                [], dtype=tf.string),
            "image/format": tf.FixedLenFeature(
                [], dtype=tf.string, default_value=self.image_format),
        }

        sequence_keys_to_features = {
            self.caption_ids_field: tf.FixedLenSequenceFeature(
                [], dtype=tf.int64),
            self.caption_tokens_field: tf.FixedLenSequenceFeature(
                [], dtype=tf.string)
        }

        items_to_handlers = {
            'image': tfexample_decoder.Image(
                image_key=self.image_field,
                format_key="image/format",
                channels=3),
            'target_ids': tfexample_decoder.Tensor(self.caption_ids_field),
            'target_tokens': tfexample_decoder.Tensor(self.caption_tokens_field),
            'target_len': tfexample_decoder.ItemHandlerCallback(
                keys=[self.caption_tokens_field],
                func=lambda x: tf.size(x[self.caption_tokens_field]))
        }

        decoder = TFSEquenceExampleDecoder(
            context_keys_to_features, sequence_keys_to_features, items_to_handlers)

        dataset = tf.contrib.slim.dataset.Dataset(
            data_sources=self.files,
            reader=tf.TFRecordReader,
            decoder=decoder,
            num_samples=None,
            items_to_descriptions={})

        return tf.contrib.slim.dataset_data_provider.DatasetDataProvider(
            dataset=dataset,
            shuffle=self.shuffle,
            num_epochs=self.num_epochs,
            **kwargs)

    @property
    def feature_keys(self):
        return {'image'}

    @property
    def label_keys(self):
        return {'target_tokens', 'target_ids', 'target_len'}


PIPELINES = {
    'ParallelTextPipeline': ParallelTextPipeline,
    'TFRecordPipeline': TFRecordPipeline,
    'ImageCaptioningPipeline': ImageCaptioningPipeline
}
