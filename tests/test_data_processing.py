# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_feature_processors, assert_equal_layers

from polyaxon_schemas.processing.feature_processors import FeatureProcessorsConfig
from polyaxon_schemas.processing.image import (
    AdjustBrightnessConfig,
    AdjustContrastConfig,
    AdjustGammaConfig,
    AdjustHueConfig,
    AdjustSaturationConfig,
    CentralCropConfig,
    ConvertColorSpaceConfig,
    ConvertImagesDtypeConfig,
    DrawBoundingBoxesConfig,
    ExtractGlimpseConfig,
    FlipConfig,
    RandomCropConfig,
    ResizeConfig,
    Rotate90Config,
    StandardizationConfig,
    ToBoundingBoxConfig,
    TotalVariationConfig,
    TransposeConfig
)
from polyaxon_schemas.processing.pipelines import (
    BasePipelineConfig,
    ImageCaptioningPipelineConfig,
    ParallelTextPipelineConfig,
    TFRecordImagePipelineConfig,
    TFRecordSequencePipelineConfig,
    TFRecordSourceSequencePipelineConfig
)


class TestFeatureProcessorsConfigs(TestCase):
    def test_feature_processors(self):
        config_dict = {
            'image1': {
                'input_layers': ['image'],
                'output_layers': ['reshap_0'],
                'layers': [
                    {'Resize': {'height': 28, 'width': 28}},
                    {'Reshape': {'target_shape': [784]}}
                ]
            },
            'image2': {
                'input_layers': ['image'],
                'output_layers': ['reshap_0'],
                'layers': [
                    {'Standardization': {}},
                    {'Resize': {'height': 28, 'width': 28}},
                    {'Reshape': {'target_shape': [784]}}
                ]
            }
        }
        config = FeatureProcessorsConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert_equal_feature_processors(config_to_dict, config_dict)


class TestPipelinesConfigs(TestCase):
    def test_base_pipeline_config(self):
        config_dict = {
            'name': 'my_pipelne',
            'num_epochs': 10,
            'shuffle': True,
            'feature_processors': {
                'image': {
                    'input_layers': ['image'],
                    'output_layers': ['reshap_0'],
                    'layers': [
                        {'Resize': {'height': 28, 'width': 28}},
                        {'Reshape': {'target_shape': [784]}}
                    ]
                },
            }
        }
        config = BasePipelineConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert config_to_dict['name'] == config_dict['name']
        assert config_to_dict['num_epochs'] == config_dict['num_epochs']
        assert config_to_dict['shuffle'] == config_dict['shuffle']

        assert_equal_feature_processors(config_to_dict['feature_processors'],
                                        config_dict['feature_processors'])

    def test_tf_record_image_pipeline_config(self):
        config_dict = {
            'batch_size': 64,
            'num_epochs': 10,
            'shuffle': True,
            'data_files': ['train_data_file'],
            'meta_data_file': 'meta_data_file',
            'feature_processors': {
                'image': {
                    'input_layers': ['image'],
                    'output_layers': ['reshap_0'],
                    'layers': [
                        {'Resize': {'height': 28, 'width': 28}},
                        {'Reshape': {'target_shape': [784]}}
                    ]
                },
            }
        }

        config = TFRecordImagePipelineConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert config_to_dict['num_epochs'] == config_dict['num_epochs']
        assert config_to_dict['shuffle'] == config_dict['shuffle']
        assert config_to_dict['data_files'] == config_dict['data_files']
        assert config_to_dict['meta_data_file'] == config_dict['meta_data_file']

        assert_equal_feature_processors(config_to_dict['feature_processors'],
                                        config_dict['feature_processors'])

    def test_tf_record_sequence_pipeline_config(self):
        config_dict = {
            'batch_size': 64,
            'num_epochs': 10,
            'shuffle': True,
            'data_files': ['train_data_file'],
            'meta_data_file': 'meta_data_file',
        }

        config = TFRecordSequencePipelineConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert config_to_dict['num_epochs'] == config_dict['num_epochs']
        assert config_to_dict['shuffle'] == config_dict['shuffle']
        assert config_to_dict['data_files'] == config_dict['data_files']
        assert config_to_dict['meta_data_file'] == config_dict['meta_data_file']

    def test_parallel_text_pipeline_config(self):
        config_dict = {
            'batch_size': 64,
            'num_epochs': 10,
            'shuffle': True,
            'source_files': ['source_data_file'],
            'target_files': ['target_data_file'],
        }

        config = ParallelTextPipelineConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert config_to_dict['num_epochs'] == config_dict['num_epochs']
        assert config_to_dict['shuffle'] == config_dict['shuffle']
        assert config_to_dict['source_files'] == config_dict['source_files']
        assert config_to_dict['target_files'] == config_dict['target_files']
        assert config_to_dict['source_delimiter'] == ""
        assert config_to_dict['target_delimiter'] == ""

    def test_tf_record_source_sequence_pipeline_config(self):
        config_dict = {
            'batch_size': 64,
            'num_epochs': 10,
            'shuffle': True,
            'files': ['source_data_file'],
            'source_field': 'source',
            'target_field': 'target'
        }

        config = TFRecordSourceSequencePipelineConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert config_to_dict['num_epochs'] == config_dict['num_epochs']
        assert config_to_dict['shuffle'] == config_dict['shuffle']
        assert config_to_dict['files'] == config_dict['files']
        assert config_to_dict['source_field'] == config_dict['source_field']
        assert config_to_dict['target_field'] == config_dict['target_field']
        assert config_to_dict['source_delimiter'] == ""
        assert config_to_dict['target_delimiter'] == ""

    def test_image_captioning_pipeline_config(self):
        config_dict = {
            'batch_size': 64,
            'num_epochs': 10,
            'shuffle': True,
            'files': ['source_data_file'],
            'image_field': 'image/data',
            'image_format': 'jpg',
            'caption_ids_field': 'image/caption_ids',
            'caption_tokens_field': 'image/caption'
        }

        config = ImageCaptioningPipelineConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert config_to_dict['num_epochs'] == config_dict['num_epochs']
        assert config_to_dict['shuffle'] == config_dict['shuffle']
        assert config_to_dict['files'] == config_dict['files']
        assert config_to_dict['image_field'] == config_dict['image_field']
        assert config_to_dict['image_format'] == config_dict['image_format']
        assert config_to_dict['caption_ids_field'] == config_dict['caption_ids_field']
        assert config_to_dict['caption_tokens_field'] == config_dict['caption_tokens_field']


class TestImageProcessingConfigs(TestCase):
    def test_resize_config(self):
        config_dict = {
            'height': 28,
            'width': 28,
            'method': 0,
            'align_corners': True,
            'name': 'Resize'
        }
        config = ResizeConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_central_crop_config(self):
        config_dict = {
            'central_fraction': 0.28,
            'name': 'CentralCrop'
        }

        config = CentralCropConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_random_crop_config(self):
        config_dict = {
            'height': 28,
            'width': 28,
            'name': 'RandomCrop'
        }

        config = RandomCropConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_extract_glimpse_config(self):
        config_dict = {
            'size': [1, 1],
            'offsets': [1, 1],
            'centered': True,
            'normalized': True,
            'uniform_noise': True,
            'name': 'ExtractGlimpse'
        }

        config = ExtractGlimpseConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_to_bounding_box_config(self):
        config_dict = {
            'offset_height': 1,
            'offset_width': 1,
            'target_height': 10,
            'target_width': 10,
            'method': 'crop',
            'name': 'ToBoundingBox'
        }

        config = ToBoundingBoxConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_flip_config(self):
        config_dict = {
            'axis': 0,
            'is_random': False,
            'seed': None,
            'name': 'Flip'
        }

        config = FlipConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_transpose_config(self):
        config_dict = {
            'name': 'Transpose'
        }

        config = TransposeConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_rotate_config(self):
        config_dict = {
            'k': 0,
            'is_random': False,
            'seed': None,
            'name': 'Rotate90'
        }

        config = Rotate90Config.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_convert_color_space_config(self):
        config_dict = {
            'from_space': 'rgb',
            'to_space': 'grayscale',
            'name': 'ConvertColorSpace'
        }

        config = ConvertColorSpaceConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_convert_image_dtype_config(self):
        config_dict = {
            'dtype': 'float32',
            'saturate': True,
            'name': 'ConvertImagesDtype'
        }

        config = ConvertImagesDtypeConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_adjust_brightness_config(self):
        config_dict = {
            'delta': 1.3,
            'is_random': True,
            'seed': 1000,
            'name': 'AdjustBrightness'
        }

        config = AdjustBrightnessConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_adjust_contrast_config(self):
        config_dict = {
            'contrast_factor': 1.3,
            'contrast_factor_max': None,
            'is_random': False,
            'seed': 1000,
            'name': 'AdjustContrast'
        }

        config = AdjustContrastConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_adjust_hue_config(self):
        config_dict = {
            'delta': 0.3,
            'is_random': True,
            'seed': 1000,
            'name': 'AdjustHue'
        }

        config = AdjustHueConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_adjust_saturation_config(self):
        config_dict = {
            'saturation_factor': 0.3,
            'saturation_factor_max': None,
            'is_random': True,
            'seed': 1000,
            'name': 'AdjustSaturation'
        }

        config = AdjustSaturationConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_adjust_gamma_config(self):
        config_dict = {
            'gamma': 0.3,
            'gain': 1,
            'name': 'AdjustGamma'
        }

        config = AdjustGammaConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_standardization_config(self):
        config_dict = {
            'name': 'Standardization'
        }

        config = StandardizationConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_draw_bounding_boxes_config(self):
        config_dict = {
            'boxes': [0, 3, 3],
            'name': 'DrawBoundingBoxes'
        }

        config = DrawBoundingBoxesConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_total_variation_config(self):
        config_dict = {
            'name': 'TotalVariation'
        }

        config = TotalVariationConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)
