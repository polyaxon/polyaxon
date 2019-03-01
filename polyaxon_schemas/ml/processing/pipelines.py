# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import EXCLUDE, fields

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema
from polyaxon_schemas.ml.processing.feature_processors import FeatureProcessorsSchema


class BasePipelineSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    feature_processors = fields.Nested(FeatureProcessorsSchema, allow_none=True)
    shuffle = fields.Bool(allow_none=True)
    num_epochs = fields.Int(allow_none=True)
    batch_size = fields.Int(allow_none=True)
    bucket_boundaries = fields.List(fields.Int(), allow_none=True)
    allow_smaller_final_batch = fields.Bool(allow_none=True)
    dynamic_pad = fields.Bool(allow_none=True)
    min_after_dequeue = fields.Int(allow_none=True)
    num_threads = fields.Int(allow_none=True)
    capacity = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return BasePipelineConfig


class BasePipelineConfig(BaseConfig):
    """Abstract InputPipeline class. All input pipelines must inherit from this.
    An InputPipeline defines how data is read, parsed, and separated into
    features and labels.

    Args:
        name: `str`, name to give for this pipeline.
        feature_processors: `dict`, list of modules to call for each feature to be processed.
        shuffle: `bool`, If true, shuffle the data.
        num_epochs: `int`, Number of times to iterate through the dataset. If None, iterate forever.
        batch_size: The new batch size pulled from the queue (all queues will have the same size).
            If a list is passed in then each bucket will have a different batch_size.
            (python int, int32 scalar or iterable of integers of length num_buckets).
        bucket_boundaries: `list` of `int` or `None`, increasing non-negative numbers.
            The edges of the buckets to use when bucketing tensors.
            Two extra buckets are created, one for input_length < bucket_boundaries[0]
            and one for input_length >= bucket_boundaries[-1].
        allow_smaller_final_batch: `bool`, whether to allow a last small batch.
        dynamic_pad: `bool`, Allow variable dimensions in input shapes.
            The given dimensions are padded upon dequeue so that tensors
            within a batch have the same shapes.
        min_after_dequeue: `int`.
        num_threads: `int`. The number of threads enqueuing tensors.
        capacity: `int`, The maximum number of minibatches in the top queue,
            and also the maximum number of elements within each bucket.
    """
    IDENTIFIER = 'BasePipeline'
    SCHEMA = BasePipelineSchema
    REDUCED_ATTRIBUTES = ['feature_processors']

    def __init__(self,
                 name='Pipeline',
                 feature_processors=None,
                 shuffle=True,
                 num_epochs=1,
                 batch_size=64,
                 bucket_boundaries=None,
                 allow_smaller_final_batch=True,
                 dynamic_pad=False,
                 min_after_dequeue=5000,
                 num_threads=3,
                 capacity=None):
        self.name = name
        self.feature_processors = feature_processors
        self.shuffle = shuffle
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.bucket_boundaries = bucket_boundaries
        self.allow_smaller_final_batch = allow_smaller_final_batch
        self.dynamic_pad = dynamic_pad
        self.min_after_dequeue = min_after_dequeue
        self.num_threads = num_threads
        self.capacity = capacity or min_after_dequeue + num_threads * batch_size


class TFRecordImagePipelineSchema(BasePipelineSchema):
    data_files = fields.List(fields.Str(), allow_none=True)
    meta_data_file = fields.Str()

    @staticmethod
    def schema_config():
        return TFRecordImagePipelineConfig


class TFRecordImagePipelineConfig(BasePipelineConfig):
    """A Pipeline to convert TF-Records to images.

    Args:
        name: `str`, name to give for this pipeline.
        feature_processors: `dict`, list of modules to call for each feature to be processed.
        shuffle: `bool`, If true, shuffle the data.
        num_epochs: `int`, Number of times to iterate through the dataset. If None, iterate forever.
        batch_size: The new batch size pulled from the queue (all queues will have the same size).
            If a list is passed in then each bucket will have a different batch_size.
            (python int, int32 scalar or iterable of integers of length num_buckets).
        bucket_boundaries: `list` of `int` or `None`, increasing non-negative numbers.
            The edges of the buckets to use when bucketing tensors.
            Two extra buckets are created, one for input_length < bucket_boundaries[0]
            and one for input_length >= bucket_boundaries[-1].
        allow_smaller_final_batch: `bool`, whether to allow a last small batch.
        dynamic_pad: `bool`, Allow variable dimensions in input shapes.
            The given dimensions are padded upon dequeue so that tensors
            within a batch have the same shapes.
        min_after_dequeue: `int`.
        num_threads: `int`. The number of threads enqueuing tensors.
        capacity: `int`, The maximum number of minibatches in the top queue,
            and also the maximum number of elements within each bucket.
        data_files: `list` of `str`. List of the filenames for data.
        meta_data_file: `str`. Metadata filename

    Polyaxonfile usage:

    ```yaml
    TFRecordImagePipeline:
      batch_size: 64
      num_epochs: 1
      shuffle: true
      dynamic_pad: false
      data_files: ["../data/mnist/mnist_train.tfrecord"]
      meta_data_file: "../data/mnist/meta_data.json"
      feature_processors:
        image:
          input_layers: [image]
          layers:
            - Cast:
                dtype: float32
    ```
    """
    IDENTIFIER = 'TFRecordImagePipeline'
    SCHEMA = TFRecordImagePipelineSchema

    def __init__(self, data_files, meta_data_file, name='TFRecordImagePipeline', **kwargs):
        super(TFRecordImagePipelineConfig, self).__init__(name=name, **kwargs)
        self.data_files = data_files
        self.meta_data_file = meta_data_file


class TFRecordSequencePipelineSchema(BasePipelineSchema):
    data_files = fields.List(fields.Str(), allow_none=True)
    meta_data_file = fields.Str()

    class Meta:
        ordered = True

    @staticmethod
    def schema_config():
        return TFRecordSequencePipelineConfig


class TFRecordSequencePipelineConfig(BasePipelineConfig):
    """A Pipeline to convert TF-Records to sequences.

    At least one sequence must be `source_token`.

    Args:
        name: `str`, name to give for this pipeline.
        feature_processors: `dict`, list of modules to call for each feature to be processed.
        shuffle: `bool`, If true, shuffle the data.
        num_epochs: `int`, Number of times to iterate through the dataset. If None, iterate forever.
        batch_size: The new batch size pulled from the queue (all queues will have the same size).
            If a list is passed in then each bucket will have a different batch_size.
            (python int, int32 scalar or iterable of integers of length num_buckets).
        bucket_boundaries: `list` of `int` or `None`, increasing non-negative numbers.
            The edges of the buckets to use when bucketing tensors.
            Two extra buckets are created, one for input_length < bucket_boundaries[0]
            and one for input_length >= bucket_boundaries[-1].
        allow_smaller_final_batch: `bool`, whether to allow a last small batch.
        dynamic_pad: `bool`, Allow variable dimensions in input shapes.
            The given dimensions are padded upon dequeue so that tensors
            within a batch have the same shapes.
        min_after_dequeue: `int`.
        num_threads: `int`. The number of threads enqueuing tensors.
        capacity: `int`, The maximum number of minibatches in the top queue,
            and also the maximum number of elements within each bucket.
        data_files: `list` of `str`. List of the filenames for data.
        meta_data_file: `str`. Metadata filename

    Polyaxonfile usage:

    ```yaml
    TFRecordSequencePipeline:
      batch_size: 64
      num_epochs: 1
      shuffle: true
      dynamic_pad: false
      data_files: ["data.tfrecord"]
      meta_data_file: "meta_data.json"
      feature_processors:
        image:
          input_layers: [sequence]
          layers:
            - Cast:
                dtype: float32
    ```
    """
    IDENTIFIER = 'TFRecordSequencePipeline'
    SCHEMA = TFRecordSequencePipelineSchema

    def __init__(self, data_files, meta_data_file, name='TFRecordSequencePipeline', **kwargs):
        super(TFRecordSequencePipelineConfig, self).__init__(name=name, **kwargs)
        self.data_files = data_files
        self.meta_data_file = meta_data_file


class ParallelTextPipelineSchema(BasePipelineSchema):
    source_files = fields.List(fields.Str(), allow_none=True)
    target_files = fields.List(fields.Str(), allow_none=True)
    source_delimiter = fields.Str(allow_none=True)
    target_delimiter = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return ParallelTextPipelineConfig


class ParallelTextPipelineConfig(BasePipelineConfig):
    """An input pipeline that reads two parallel (line-by-line aligned) text files.

    Args:
        name: `str`, name to give for this pipeline.
        feature_processors: `dict`, list of modules to call for each feature to be processed.
        shuffle: `bool`, If true, shuffle the data.
        num_epochs: `int`, Number of times to iterate through the dataset. If None, iterate forever.
        batch_size: The new batch size pulled from the queue (all queues will have the same size).
            If a list is passed in then each bucket will have a different batch_size.
            (python int, int32 scalar or iterable of integers of length num_buckets).
        bucket_boundaries: `list` of `int` or `None`, increasing non-negative numbers.
            The edges of the buckets to use when bucketing tensors.
            Two extra buckets are created, one for input_length < bucket_boundaries[0]
            and one for input_length >= bucket_boundaries[-1].
        allow_smaller_final_batch: `bool`, whether to allow a last small batch.
        dynamic_pad: `bool`, Allow variable dimensions in input shapes.
            The given dimensions are padded upon dequeue so that tensors
            within a batch have the same shapes.
        min_after_dequeue: `int`.
        num_threads: `int`. The number of threads enqueuing tensors.
        capacity: `int`, The maximum number of minibatches in the top queue,
            and also the maximum number of elements within each bucket.
        source_files: An array of file names for the source data.
        target_files: An array of file names for the target data. These must
          be aligned to the `source_files`.
        source_delimiter: A character to split the source text on. Defaults
          to  " " (space). For character-level training this can be set to the
          empty string.
        target_delimiter: Same as `source_delimiter` but for the target text.
    """
    IDENTIFIER = 'ParallelTextPipeline'
    SCHEMA = ParallelTextPipelineSchema

    def __init__(self,
                 source_files=None,
                 target_files=None,
                 source_delimiter="",
                 target_delimiter="",
                 name='ParallelTextPipeline',
                 **kwargs):
        super(ParallelTextPipelineConfig, self).__init__(name=name, **kwargs)
        self.source_files = source_files
        self.target_files = target_files
        self.source_delimiter = source_delimiter
        self.target_delimiter = target_delimiter


class TFRecordSourceSequencePipelineSchema(BasePipelineSchema):
    files = fields.List(fields.Str(), allow_none=True)
    source_field = fields.Str(allow_none=True)
    target_field = fields.Str(allow_none=True)
    source_delimiter = fields.Str(allow_none=True)
    target_delimiter = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return TFRecordSourceSequencePipelineConfig


class TFRecordSourceSequencePipelineConfig(BasePipelineConfig):
    """An input pipeline that reads a TFRecords containing both source and target sequences.

    Args:
        name: `str`, name to give for this pipeline.
        feature_processors: `dict`, list of modules to call for each feature to be processed.
        shuffle: `bool`, If true, shuffle the data.
        num_epochs: `int`, Number of times to iterate through the dataset. If None, iterate forever.
        batch_size: The new batch size pulled from the queue (all queues will have the same size).
            If a list is passed in then each bucket will have a different batch_size.
            (python int, int32 scalar or iterable of integers of length num_buckets).
        bucket_boundaries: `list` of `int` or `None`, increasing non-negative numbers.
            The edges of the buckets to use when bucketing tensors.
            Two extra buckets are created, one for input_length < bucket_boundaries[0]
            and one for input_length >= bucket_boundaries[-1].
        allow_smaller_final_batch: `bool`, whether to allow a last small batch.
        dynamic_pad: `bool`, Allow variable dimensions in input shapes.
            The given dimensions are padded upon dequeue so that tensors
            within a batch have the same shapes.
        min_after_dequeue: `int`.
        num_threads: `int`. The number of threads enqueuing tensors.
        capacity: `int`, The maximum number of minibatches in the top queue,
            and also the maximum number of elements within each bucket.
        source_field: The TFRecord feature field containing the source text.
        target_field: The TFRecord feature field containing the target text.
        source_delimiter: A character to split the source text on. Defaults
          to  " " (space). For character-level training this can be set to the
          empty string.
        target_delimiter: Same as `source_delimiter` but for the target text.
    """
    IDENTIFIER = 'TFRecordSourceSequencePipeline'
    SCHEMA = TFRecordSourceSequencePipelineSchema

    def __init__(self,
                 files=None,
                 source_field='source',
                 target_field='target',
                 source_delimiter="",
                 target_delimiter="",
                 name='TFRecordSourceSequencePipeline',
                 **kwargs):
        super(TFRecordSourceSequencePipelineConfig, self).__init__(name=name, **kwargs)
        self.files = files
        self.source_field = source_field
        self.target_field = target_field
        self.source_delimiter = source_delimiter
        self.target_delimiter = target_delimiter


class ImageCaptioningPipelineSchema(BasePipelineSchema):
    files = fields.List(fields.Str(), allow_none=True)
    image_field = fields.Str(allow_none=True)
    image_format = fields.Str(allow_none=True)
    caption_ids_field = fields.Str(allow_none=True)
    caption_tokens_field = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return ImageCaptioningPipelineConfig


class ImageCaptioningPipelineConfig(BasePipelineConfig):
    """An input pipeline that reads a TFRecords containing both source and target sequences.

    Args:
        name: `str`, name to give for this pipeline.
        feature_processors: `dict`, list of modules to call for each feature to be processed.
        shuffle: `bool`, If true, shuffle the data.
        num_epochs: `int`, Number of times to iterate through the dataset. If None, iterate forever.
        batch_size: The new batch size pulled from the queue (all queues will have the same size).
            If a list is passed in then each bucket will have a different batch_size.
            (python int, int32 scalar or iterable of integers of length num_buckets).
        bucket_boundaries: `list` of `int` or `None`, increasing non-negative numbers.
            The edges of the buckets to use when bucketing tensors.
            Two extra buckets are created, one for input_length < bucket_boundaries[0]
            and one for input_length >= bucket_boundaries[-1].
        allow_smaller_final_batch: `bool`, whether to allow a last small batch.
        dynamic_pad: `bool`, Allow variable dimensions in input shapes.
            The given dimensions are padded upon dequeue so that tensors
            within a batch have the same shapes.
        min_after_dequeue: `int`.
        num_threads: `int`. The number of threads enqueuing tensors.
        capacity: `int`, The maximum number of minibatches in the top queue,
            and also the maximum number of elements within each bucket.
        files: An array of file names to read from.
        image_field: The TFRecord feature field containing the source images.
        image_format: The images extensions.
        caption_ids_field: The caption ids field.
        caption_tokens_field: the caption tokends field.
    """
    IDENTIFIER = 'ImageCaptioningPipeline'
    SCHEMA = ImageCaptioningPipelineSchema

    def __init__(self,
                 files=None,
                 image_field="image/data",
                 image_format='jpg',
                 caption_ids_field="image/caption_ids",
                 caption_tokens_field="image/caption",
                 name='ImageCaptioningPipeline',
                 **kwargs):
        super(ImageCaptioningPipelineConfig, self).__init__(name=name, **kwargs)
        self.files = files
        self.image_field = image_field
        self.image_format = image_format
        self.caption_ids_field = caption_ids_field
        self.caption_tokens_field = caption_tokens_field


class PipelineSchema(BaseMultiSchema):
    __multi_schema_name__ = 'pipeline'
    __configs__ = {
        TFRecordImagePipelineConfig.IDENTIFIER: TFRecordImagePipelineConfig,
        TFRecordSequencePipelineConfig.IDENTIFIER: TFRecordSequencePipelineConfig,
        ParallelTextPipelineConfig.IDENTIFIER: ParallelTextPipelineConfig,
        TFRecordSourceSequencePipelineConfig.IDENTIFIER: TFRecordSourceSequencePipelineConfig,
        ImageCaptioningPipelineConfig.IDENTIFIER: ImageCaptioningPipelineConfig,
    }


class PipelineConfig(BaseConfig):
    SCHEMA = PipelineSchema
    IDENTIFIER = 'pipeline'
    UNKNOWN_BEHAVIOUR = EXCLUDE
