# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.ops import params as ops_params
from polyaxon_schemas.ops.io import IOTypes
from polyaxon_schemas.ops.operation import BaseOpConfig


class TestOperationsConfigs(TestCase):
    def test_passing_params_declarations_raises(self):
        config_dict = {
            'params': {'foo': 'bar'},
            'declarations': {'foo': 'bar'},
        }

        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

    def test_passing_declarations_sets_params(self):
        config_dict = {
            'declarations': {'foo': 'bar'},
        }

        op = BaseOpConfig.from_dict(config_dict)
        assert op.params == config_dict['declarations']

    def test_passing_params_passes(self):
        config_dict = {
            'params': {'foo': 'bar'},
        }

        op = BaseOpConfig.from_dict(config_dict)
        assert op.params == config_dict['params']

    def test_param_validation_with_inputs(self):
        config_dict = {
            'params': {
                'param1': 'text',
                'param2': 12,
                'param3': 13.3,
                'param4': False,
                'param5': {'foo': 'bar'},
                'param6': [1, 3, 45, 5],
                'param7': 'gs://bucket/path/to/blob/',
                'param8': 's3://test/this/is/bad/key.txt',
                'param9': 'wasbs://container@user.blob.core.windows.net/',
                'param10': '/foo/bar'
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.STR},
                {'name': 'param2', 'type': IOTypes.INT},
                {'name': 'param3', 'type': IOTypes.FLOAT},
                {'name': 'param4', 'type': IOTypes.BOOL},
                {'name': 'param5', 'type': IOTypes.DICT},
                {'name': 'param6', 'type': IOTypes.LIST},
                {'name': 'param7', 'type': IOTypes.GCS_PATH},
                {'name': 'param8', 'type': IOTypes.S3_PATH},
                {'name': 'param9', 'type': IOTypes.AZURE_PATH},
                {'name': 'param10', 'type': IOTypes.PATH},
            ]
        }
        op = BaseOpConfig.from_dict(config_dict)
        assert op.params == config_dict['params']

    def test_param_validation_with_outputs(self):
        config_dict = {
            'params': {
                'param1': 'text',
                'param2': 12,
                'param3': 13.3,
                'param4': False,
                'param5': {'foo': 'bar'},
                'param6': [1, 3, 45, 5],
                'param7': 'gs://bucket/path/to/blob/',
                'param8': 's3://test/this/is/bad/key.txt',
                'param9': 'wasbs://container@user.blob.core.windows.net/',
                'param10': '/foo/bar',
                'param11': 124.4,
                'param12': {'foo': 124.4},
                'param13': {'foo': 'bar'},
                'param14': {'foo': ['foo', 124.4]},
            },
            'outputs': [
                {'name': 'param1', 'type': IOTypes.STR},
                {'name': 'param2', 'type': IOTypes.INT},
                {'name': 'param3', 'type': IOTypes.FLOAT},
                {'name': 'param4', 'type': IOTypes.BOOL},
                {'name': 'param5', 'type': IOTypes.DICT},
                {'name': 'param6', 'type': IOTypes.LIST},
                {'name': 'param7', 'type': IOTypes.GCS_PATH},
                {'name': 'param8', 'type': IOTypes.S3_PATH},
                {'name': 'param9', 'type': IOTypes.AZURE_PATH},
                {'name': 'param10', 'type': IOTypes.PATH},
                {'name': 'param11', 'type': IOTypes.METRIC},
                {'name': 'param12', 'type': IOTypes.METADATA},
                {'name': 'param13', 'type': IOTypes.METADATA},
                {'name': 'param14', 'type': IOTypes.METADATA},
            ]
        }
        op = BaseOpConfig.from_dict(config_dict)
        assert op.params == config_dict['params']

    def test_required_input_no_param_only_validated_on_run(self):
        # Inputs
        config_dict = {
            'params': {
                'param1': 'text',
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.STR},
                {'name': 'param10', 'type': IOTypes.PATH},
            ]
        }
        config = BaseOpConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(params=config.params,
                                       inputs=config.inputs,
                                       outputs=config.outputs,
                                       is_template=False,
                                       is_run=True)

        # Outputs
        config_dict = {
            'params': {
                'param1': 'text',
            },
            'outputs': [
                {'name': 'param1', 'type': IOTypes.STR},
                {'name': 'param10', 'type': IOTypes.PATH},
            ]
        }
        config = BaseOpConfig.from_dict(config_dict)

        ops_params.validate_params(params=config.params,
                                   inputs=config.inputs,
                                   outputs=config.outputs,
                                   is_template=False,
                                   is_run=True)

        # IO
        config_dict = {
            'params': {
                'param1': 'text',
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.STR},
            ],
            'outputs': [
                {'name': 'param10', 'type': IOTypes.PATH},
            ]
        }
        config = BaseOpConfig.from_dict(config_dict)
        ops_params.validate_params(params=config.params,
                                   inputs=config.inputs,
                                   outputs=config.outputs,
                                   is_template=False,
                                   is_run=True)

    def test_incomplete_params(self):
        config_dict = {
            'params': {
                'param1': 1,
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.INT},
                {'name': 'param2', 'type': IOTypes.INT},
            ]
        }
        config = BaseOpConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            ops_params.validate_params(params=config.params,
                                       inputs=config.inputs,
                                       outputs=config.outputs,
                                       is_template=False,
                                       is_run=True)

        config_dict = {
            'params': {
                'param1': 1,
            },
            'outputs': [
                {'name': 'param1', 'type': IOTypes.INT, 'default': 12, 'is_optional': True},
                {'name': 'param2', 'type': IOTypes.INT},
            ]
        }
        config = BaseOpConfig.from_dict(config_dict)
        ops_params.validate_params(params=config.params,
                                   inputs=config.inputs,
                                   outputs=config.outputs,
                                   is_template=False,
                                   is_run=True)

    def test_extra_params(self):
        # inputs
        config_dict = {
            'params': {
                'param1': 1,
                'param2': 2,
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        # outputs
        config_dict = {
            'params': {
                'param1': 1,
                'param2': 2,
            },
            'outputs': [
                {'name': 'param1', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

    def test_param_validation_with_mismatched_inputs(self):
        config_dict = {
            'params': {
                'param1': 'text',
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param2': 12,
            },
            'inputs': [
                {'name': 'param2', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param3': 13.3,
            },
            'inputs': [
                {'name': 'param3', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param4': False,
            },
            'inputs': [
                {'name': 'param4', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param5': {'foo': 'bar'},
            },
            'inputs': [
                {'name': 'param5', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param6': [1, 3, 45, 5],
            },
            'inputs': [
                {'name': 'param6', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param7': 'gs://bucket/path/to/blob/',
            },
            'inputs': [
                {'name': 'param7', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param8': 's3://test/this/is/bad/key.txt',
            },
            'inputs': [
                {'name': 'param8', 'type': IOTypes.AZURE_PATH},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param9': 'wasbs://container@user.blob.core.windows.net/',
            },
            'inputs': [
                {'name': 'param9', 'type': IOTypes.FLOAT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

    def test_param_validation_with_mismatched_outputs(self):
        config_dict = {
            'params': {
                'param1': 'text',
            },
            'outputs': [
                {'name': 'param1', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param2': 12,
            },
            'outputs': [
                {'name': 'param2', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param3': 13.3,
            },
            'outputs': [
                {'name': 'param3', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param4': False,
            },
            'outputs': [
                {'name': 'param4', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param5': {'foo': 'bar'},
            },
            'outputs': [
                {'name': 'param5', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param6': [1, 3, 45, 5],
            },
            'outputs': [
                {'name': 'param6', 'type': IOTypes.STR},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param7': 'gs://bucket/path/to/blob/',
            },
            'outputs': [
                {'name': 'param7', 'type': IOTypes.INT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param8': 's3://test/this/is/bad/key.txt',
            },
            'outputs': [
                {'name': 'param8', 'type': IOTypes.AZURE_PATH},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param9': 'wasbs://container@user.blob.core.windows.net/',
            },
            'outputs': [
                {'name': 'param9', 'type': IOTypes.FLOAT},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param12': 'wasbs://container@user.blob.core.windows.net/',
            },
            'outputs': [
                {'name': 'param12', 'type': IOTypes.METADATA},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'params': {
                'param9': 'wasbs://container@user.blob.core.windows.net/',
            },
            'outputs': [
                {'name': 'param9', 'type': IOTypes.METRIC},
            ]
        }
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

    def test_experiment_and_job_refs_params(self):
        config_dict = {
            'params': {
                'param1': '{{ experiments.1.outputs.foo }}',
                'param2': '{{ jobs.1.outputs.foo }}',
                'param9': 'wasbs://container@user.blob.core.windows.net/',
                'param11': '{{ experiments.1.outputs.accuracy }}',
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.INT},
                {'name': 'param2', 'type': IOTypes.FLOAT},
                {'name': 'param9', 'type': IOTypes.AZURE_PATH},
                {'name': 'param11', 'type': IOTypes.METRIC},
            ],
        }
        op = BaseOpConfig.from_dict(config_dict)
        assert op.params == config_dict['params']

    def test_op_refs_params(self):
        config_dict = {
            'params': {
                'param1': '{{ ops.A.outputs.foo }}',
                'param9': 13.1,
            },
            'inputs': [
                {'name': 'param1', 'type': IOTypes.INT},
                {'name': 'param9', 'type': IOTypes.FLOAT},
            ]
        }
        # Validation outside the context of a pipeline
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)
