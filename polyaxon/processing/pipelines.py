# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import tensorflow as tf
from tensorflow.contrib import slim as tfslim

from polyaxon.libs.template_module import GraphModule
from polyaxon.processing.data_decoders import (
    SplitTokensDecoder,
    TFExampleDecoder,
    TFSequenceExampleDecoder,
)
from polyaxon.processing.data_providers import ParallelDatasetProvider, DatasetDataProvider, Dataset
from polyaxon.processing.image import Flip


class Pipeline(GraphModule):
    """Abstract InputPipeline class. All input pipelines must inherit from this.
    An InputPipeline defines how data is read, parsed, and separated into
    features and labels.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`, name to give for this pipeline.
        subgraphs_by_features: `dict`, list of modules to call for each feature to be processed.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
    """

    def __init__(self, mode, name='Pipeline', subgraphs_by_features=None, shuffle=True,
                 num_epochs=None):
        super(Pipeline, self).__init__(
            mode=mode, name=name, module_type=GraphModule.ModuleType.PIPELINE)
        self.subgraphs_by_features = subgraphs_by_features
        self.shuffle = shuffle
        self.num_epochs = num_epochs

    def make_data_provider(self, **kwargs):
        """Creates DataProvider instance for this input pipeline. Additional keyword arguments
        are passed to the DataProvider.
        """
        raise NotImplementedError("Not implemented.")

    @property
    def feature_keys(self):
        """Defines the features that this input pipeline provides. Returns a set of strings."""
        return set()

    @property
    def label_keys(self):
        """Defines the labels that this input pipeline provides. Returns
          a set of strings.
        """
        return set()

    def _build(self, incoming, *args, **kwargs):
        for feature, subgraph in self.subgraphs_by_features.items():
            if feature not in incoming:
                raise KeyError("The feature `{}` does not exist, please review your pipeline "
                               "feature processors".format(feature))
            incoming[feature] = subgraph(incoming[feature])
        return incoming

    @staticmethod
    def read_from_data_provider(data_provider):
        """Utility function to read all available items from a DataProvider."""
        item_values = data_provider.get(list(data_provider.list_items()))
        items_dict = dict(zip(data_provider.list_items(), item_values))
        return items_dict


class TFRecordImagePipeline(Pipeline):
    """Abstract InputPipeline class. All input pipelines must inherit from this.
    An InputPipeline defines how data is read, parsed, and separated into
    features and labels.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`, name to give for this pipeline.
        subgraphs_by_features: `dict`, list of modules to call for each feature to be processed
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
    """

    def __init__(self, mode, name='TFRecordImagePipeline', subgraphs_by_features=None, shuffle=True,
                 num_epochs=None, data_files=None, meta_data_file=None):
        super(TFRecordImagePipeline, self).__init__(
            mode=mode, name=name, subgraphs_by_features=subgraphs_by_features,
            shuffle=shuffle, num_epochs=num_epochs)
        self.data_files = data_files or []
        self.meta_data = None
        if meta_data_file:
            with open(meta_data_file) as meta_data_file:
                self.meta_data = json.load(meta_data_file)

    def make_data_provider(self, **kwargs):
        """Creates DataProvider instance for this input pipeline. Additional keyword arguments
        are passed to the DataProvider.
        """
        keys_to_features = {
            'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
            'image/format': tf.FixedLenFeature((), tf.string,
                                               default_value=self.meta_data.get('image_format')),
            'image/class/label': tf.FixedLenFeature(
                [1], tf.int64, default_value=tf.zeros([1], dtype=tf.int64)),
        }

        image_shape = [self.meta_data.get('height'),
                       self.meta_data.get('width'),
                       self.meta_data.get('channels')]
        if not all(image_shape):
            # no reshaping should be done
            image_shape = None

        items_to_handlers = {
            'image': tfslim.tfexample_decoder.Image(shape=image_shape,
                                                    channels=self.meta_data.get('channels')),
            'label': tfslim.tfexample_decoder.Tensor('image/class/label', shape=[]),
        }

        decoder = TFExampleDecoder(keys_to_features, items_to_handlers)

        dataset = Dataset(
            data_sources=self.data_files,
            reader=tf.TFRecordReader,
            decoder=decoder,
            num_samples=self.meta_data.get('num_samples', {}).get(self.mode),
            num_classes=self.meta_data['num_classes'],
            items_to_descriptions=self.meta_data.get('items_to_descriptions', {}),
            meta_data=self.meta_data,
            labels_to_names=self.meta_data['labels_to_classes'])

        return DatasetDataProvider(dataset=dataset, shuffle=self.shuffle,
                                   num_epochs=self.num_epochs, **kwargs)

    @property
    def feature_keys(self):
        """Defines the features that this input pipeline provides. Returns a set of strings."""
        return {'image'}

    @property
    def label_keys(self):
        """Defines the labels that this input pipeline provides. Returns a set of strings."""
        return {'label'}


class ParallelTextPipeline(Pipeline):
    """An input pipeline that reads two parallel (line-by-line aligned) text files.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`, name to give for this pipeline.
        subgraphs_by_features: `dict`, list of modules to call for each feature to be processed
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
    def __init__(self, mode, name='ParallelTextPipeline', subgraphs_by_features=None, shuffle=True,
                 num_epochs=None, source_files=None, target_files=None, source_delimiter="",
                 target_delimiter=""):
        super(ParallelTextPipeline, self).__init__(
            mode=mode, name=name, subgraphs_by_features=subgraphs_by_features, shuffle=shuffle,
            num_epochs=num_epochs)
        self.source_files = source_files or []
        self.target_files = target_files or []
        self.source_delimiter = source_delimiter
        self.target_delimiter = target_delimiter

    def make_data_provider(self, **kwargs):
        """Creates DataProvider instance for this input pipeline. Additional keyword arguments
        are passed to the DataProvider.
        """
        decoder_source = SplitTokensDecoder(
            tokens_feature_name='source_tokens',
            length_feature_name='source_len',
            append_token='SEQUENCE_END',
            delimiter=self.source_delimiter)

        dataset_source = Dataset(
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

            dataset_target = Dataset(
                data_sources=self.target_files,
                reader=tf.TextLineReader,
                decoder=decoder_target,
                num_samples=None,
                items_to_descriptions={})

        return ParallelDatasetProvider(
            dataset_source=dataset_source,
            dataset_target=dataset_target,
            shuffle=self.shuffle,
            num_epochs=self.num_epochs,
            **kwargs)

    @property
    def feature_keys(self):
        """Defines the features that this input pipeline provides. Returns a set of strings."""
        return {'source_tokens', 'source_len'}

    @property
    def label_keys(self):
        """Defines the labels that this input pipeline provides. Returns a set of strings."""
        return {'target_tokens', 'target_len'}


class TFRecordSourceSequencePipeline(Pipeline):
    """An input pipeline that reads a TFRecords containing both source and target sequences.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`, name to give for this pipeline.
        subgraphs_by_features: `dict`, list of modules to call for each feature to be processed
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

    def __init__(self, mode, name='TFRecordSourceSequencePipeline', subgraphs_by_features=None,
                 shuffle=True, num_epochs=None, files=None, source_field='source',
                 target_field='target', source_delimiter="", target_delimiter=""):
        self.files = files or []
        self.source_field = source_field
        self.target_field = target_field
        self.source_delimiter = source_delimiter
        self.target_delimiter = target_delimiter
        super(TFRecordSourceSequencePipeline, self).__init__(
            mode=mode, name=name, subgraphs_by_features=subgraphs_by_features,
            shuffle=shuffle, num_epochs=num_epochs)

    def make_data_provider(self, **kwargs):
        """Creates DataProvider instance for this input pipeline. Additional keyword arguments
        are passed to the DataProvider.
        """
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
            self.target_field: tf.FixedLenFeature((), tf.string, default_value="")
        }

        items_to_handlers = {
            'source_tokens': tfslim.tfexample_decoder.ItemHandlerCallback(
                keys=[self.source_field],
                func=lambda dict: splitter_source.decode(dict[self.source_field],
                                                         ['source_tokens'])[0]),
            'source_len': tfslim.tfexample_decoder.ItemHandlerCallback(
                keys=[self.source_field],
                func=lambda dict: splitter_source.decode(dict[self.source_field],
                                                         ['source_len'])[0]),
            'target_tokens': tfslim.tfexample_decoder.ItemHandlerCallback(
                keys=[self.target_field],
                func=lambda dict: splitter_target.decode(dict[self.target_field],
                                                         ['target_tokens'])[0]),
            'target_len': tfslim.tfexample_decoder.ItemHandlerCallback(
                keys=[self.target_field],
                func=lambda dict: splitter_target.decode(dict[self.target_field],
                                                         ['target_len'])[0])
        }

        decoder = TFExampleDecoder(keys_to_features, items_to_handlers)

        dataset = Dataset(data_sources=self.files, reader=tf.TFRecordReader, decoder=decoder)

        return DatasetDataProvider(dataset=dataset, shuffle=self.shuffle,
                                   num_epochs=self.num_epochs, **kwargs)

    @property
    def feature_keys(self):
        """Defines the features that this input pipeline provides. Returns a set of strings."""
        return {'source_tokens', 'source_len'}

    @property
    def label_keys(self):
        """Defines the labels that this input pipeline provides. Returns a set of strings."""
        return {'target_tokens', 'target_len'}


class ImageCaptioningPipeline(Pipeline):
    """An input pipeline that reads a TFRecords containing both source and target sequences.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`, name to give for this pipeline.
        subgraphs_by_features: `dict`, list of modules to call for each feature to be processed
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
        files: An array of file names to read from.
        image_field: The TFRecord feature field containing the source images.
        image_format: The images extensions.
        caption_ids_field: The caption ids field.
        caption_tokens_field: the caption tokends field.
    """

    def __init__(self, mode, name='ImageCaptioningPipeline',  subgraphs_by_features=None,
                 shuffle=True, num_epochs=None, files=None, image_field="image/data",
                 image_format='jpg', caption_ids_field="image/caption_ids",
                 caption_tokens_field="image/caption"):
        self.files = files or []
        self.image_field = image_field
        self.image_format = image_format
        self.caption_ids_field = caption_ids_field
        self.caption_tokens_field = caption_tokens_field
        super(ImageCaptioningPipeline).__init__(
            mode=mode, name=name, subgraphs_by_features=subgraphs_by_features, shuffle=shuffle,
            num_epochs=num_epochs)

    def make_data_provider(self, **kwargs):
        """Creates DataProvider instance for this input pipeline. Additional keyword arguments
        are passed to the DataProvider.
        """
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
            'image': tfslim.tfexample_decoder.Image(
                image_key=self.image_field,
                format_key="image/format",
                channels=3),
            'target_ids': tfslim.tfexample_decoder.Tensor(self.caption_ids_field),
            'target_tokens': tfslim.tfexample_decoder.Tensor(self.caption_tokens_field),
            'target_len': tfslim.tfexample_decoder.ItemHandlerCallback(
                keys=[self.caption_tokens_field],
                func=lambda x: tf.size(x[self.caption_tokens_field]))
        }

        decoder = TFSequenceExampleDecoder(
            context_keys_to_features, sequence_keys_to_features, items_to_handlers)

        dataset = Dataset(
            data_sources=self.files,
            reader=tf.TFRecordReader,
            decoder=decoder,
            num_samples=None,
            items_to_descriptions={})

        return DatasetDataProvider(
            dataset=dataset,
            shuffle=self.shuffle,
            num_epochs=self.num_epochs,
            **kwargs)

    @property
    def feature_keys(self):
        """Defines the features that this input pipeline provides. Returns a set of strings."""
        return {'image'}

    @property
    def label_keys(self):
        """Defines the labels that this input pipeline provides. Returns a set of strings."""
        return {'target_tokens', 'target_ids', 'target_len'}


PIPELINES = {
    'ParallelTextPipeline': ParallelTextPipeline,
    'TFRecordImagePipeline': TFRecordImagePipeline,
    'TFRecordSourceSequencePipeline': TFRecordSourceSequencePipeline,
    'ImageCaptioningPipeline': ImageCaptioningPipeline
}
