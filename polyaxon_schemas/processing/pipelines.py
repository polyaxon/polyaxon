# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.processing.feature_processors import FeatureProcessorsSchema


class BasePipelineSchema(Schema):
    name = fields.Str(allow_none=True)
    feature_processors = fields.Nested(FeatureProcessorsSchema, allow_none=True)
    shuffle = fields.Bool(allow_none=True)
    num_epochs = fields.Int(allow_none=True)
    batch_size = fields.Int(allow_none=True)
    bucket_boundaries = fields.List(fields.Int, allow_none=True)
    allow_smaller_final_batch = fields.Bool(allow_none=True)
    dynamic_pad = fields.Bool(allow_none=True)
    min_after_dequeue = fields.Int(allow_none=True)
    num_threads = fields.Int(allow_none=True)
    capacity = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return BasePipelineConfig(**data)


class BasePipelineConfig(BaseConfig):
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
    data_files = fields.List(fields.Str, allow_none=True)
    meta_data_file = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TFRecordImagePipelineConfig(**data)


class TFRecordImagePipelineConfig(BasePipelineConfig):
    IDENTIFIER = 'TFRecordImagePipeline'
    SCHEMA = TFRecordImagePipelineSchema

    def __init__(self, data_files, meta_data_file, name='TFRecordImagePipeline', **kwargs):
        super(TFRecordImagePipelineConfig, self).__init__(name=name, **kwargs)
        self.data_files = data_files
        self.meta_data_file = meta_data_file


class TFRecordSequencePipelineSchema(BasePipelineSchema):
    data_files = fields.List(fields.Str, allow_none=True)
    meta_data_file = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TFRecordSequencePipelineConfig(**data)


class TFRecordSequencePipelineConfig(BasePipelineConfig):
    IDENTIFIER = 'TFRecordSequencePipeline'
    SCHEMA = TFRecordSequencePipelineSchema

    def __init__(self, data_files, meta_data_file, name='TFRecordSequencePipeline', **kwargs):
        super(TFRecordSequencePipelineConfig, self).__init__(name=name, **kwargs)
        self.data_files = data_files
        self.meta_data_file = meta_data_file


class ParallelTextPipelineSchema(BasePipelineSchema):
    source_files = fields.List(fields.Str, allow_none=True)
    target_files = fields.List(fields.Str, allow_none=True)
    source_delimiter = fields.Str(allow_none=True)
    target_delimiter = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ParallelTextPipelineConfig(**data)


class ParallelTextPipelineConfig(BasePipelineConfig):
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
    files = fields.List(fields.Str, allow_none=True)
    source_field = fields.Str(allow_none=True)
    target_field = fields.Str(allow_none=True)
    source_delimiter = fields.Str(allow_none=True)
    target_delimiter = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TFRecordSourceSequencePipelineConfig(**data)


class TFRecordSourceSequencePipelineConfig(BasePipelineConfig):
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
    files = fields.List(fields.Str, allow_none=True)
    image_field = fields.Str(allow_none=True)
    image_format = fields.Str(allow_none=True)
    caption_ids_field = fields.Str(allow_none=True)
    caption_tokens_field = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ImageCaptioningPipelineConfig(**data)


class ImageCaptioningPipelineConfig(BasePipelineConfig):
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
