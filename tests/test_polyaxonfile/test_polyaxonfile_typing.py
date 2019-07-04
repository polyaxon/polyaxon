# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from flaky import flaky

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.ops.build_job import BuildConfig
from polyaxon_schemas.ops.environments.pods import EnvironmentConfig
from polyaxon_schemas.ops.environments.resources import K8SResourcesConfig, PodResourcesConfig
from polyaxon_schemas.ops.experiment.backends import ExperimentBackend
from polyaxon_schemas.ops.experiment.frameworks import ExperimentFramework
from polyaxon_schemas.ops.group.early_stopping_policies import EarlyStoppingConfig
from polyaxon_schemas.ops.group.hptuning import HPTuningConfig, SearchAlgorithms
from polyaxon_schemas.ops.group.matrix import MatrixConfig
from polyaxon_schemas.ops.logging import LoggingConfig
from polyaxon_schemas.ops.run import RunConfig
from polyaxon_schemas.polyaxonfile import PolyaxonFile
from polyaxon_schemas.specs.frameworks import (
    HorovodSpecification,
    MPISpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from polyaxon_schemas.utils import TaskType


class TestPolyaxonfileWithTypes(TestCase):
    def test_using_untyped_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/typing/untyped_params.yml'))

    def test_no_params_for_required_inputs_outputs_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath(
                'tests/fixtures/typing/required_inputs.yml'))

        PolyaxonFile(os.path.abspath(
            'tests/fixtures/typing/required_outputs.yml'))

    def test_required_inputs_with_params(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/typing/required_inputs.yml'),
                               params={'loss': 'bar', 'flag': False})
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert set(spec.tags) == {'foo', 'bar'}
        assert spec.params == {'loss': 'bar', 'flag': ''}
        assert spec.build.image == 'my_image'
        assert spec.run.cmd == 'video_prediction_train --loss=bar '
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_experiment
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.is_experiment is True

        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/typing/required_inputs.yml'),
                               params={'loss': 'bar', 'flag': True})
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert set(spec.tags) == {'foo', 'bar'}
        assert spec.params == {'loss': 'bar', 'flag': '--flag'}
        assert spec.build.image == 'my_image'
        assert spec.run.cmd == 'video_prediction_train --loss=bar --flag'
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_experiment
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.is_experiment is True

        # Adding extra value raises
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/typing/required_inputs.yml'),
                         params={'loss': 'bar', 'value': 1.1})

        # Adding non valid params raises
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/typing/required_inputs.yml'),
                         params={'value': 1.1})

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/typing/matrix_file_with_int_float_types.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['param1'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['param2'], MatrixConfig)
        assert spec.hptuning.matrix['param1'].to_dict() == {'values': [1, 2]}
        assert spec.hptuning.matrix['param2'].to_dict() == {'values': [3.3, 4.4]}
        assert spec.matrix_space == 4
        assert isinstance(spec.hptuning, HPTuningConfig)
        assert spec.hptuning.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.GRID
        assert spec.hptuning.early_stopping is None
        assert spec.early_stopping == []

        assert spec.experiments_def == {
            'search_algorithm': SearchAlgorithms.GRID,
            'early_stopping': False,
            'concurrency': 2,
        }

        build = spec.build
        assert build is None

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        spec.apply_context()
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.run.cmd == 'train --param1={param1} --param2={param2} --param3=23423'.format(
            **spec.params
        )

    def test_run_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/typing/run_cmd_simple_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.is_experiment
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        assert run.cmd == "video_prediction_train --num_masks=2 --loss=MeanSquaredError"

    def test_run_with_refs(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/typing/run_with_refs.yml'))
        spec = plxfile.specification
        required_refs = spec.raw_config.get_params_with_refs()
        assert len(required_refs) == 1
        assert required_refs[0].name == 'model_path'
        assert required_refs[0].value == 'jobs.1.outputs.doo'
        spec.apply_context(context={'jobs__1__outputs__doo': 'model_path'})
        assert spec.version == 1
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.is_experiment
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        assert run.cmd == "video_prediction_train --num_masks=2 --model_path=model_path"

    def test_jupyter_lab_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/typing/jupyterlab_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_notebook
        assert spec.is_notebook is True
        assert spec.backend == 'lab'
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        assert spec.secret_refs == ['secret1', 'secret2']
        assert spec.config_map_refs == ['config_map1', 'config_map2']

        node_selector = {'polyaxon.com': 'node_for_notebook_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations
