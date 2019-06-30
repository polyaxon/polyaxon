# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from flaky import flaky

from polyaxon_schemas.ops.build_job import BuildConfig
from polyaxon_schemas.ops.environments.pods import EnvironmentConfig
from polyaxon_schemas.ops.environments.resources import K8SResourcesConfig, PodResourcesConfig
from polyaxon_schemas.ops.experiment.frameworks import ExperimentFramework
from polyaxon_schemas.ops.group.early_stopping_policies import EarlyStoppingConfig
from polyaxon_schemas.ops.group.hptuning import HPTuningConfig, SearchAlgorithms
from polyaxon_schemas.ops.group.matrix import MatrixConfig
from polyaxon_schemas.ops.logging import LoggingConfig
from polyaxon_schemas.polyaxonfile import PolyaxonFile
from polyaxon_schemas.specs.frameworks import TensorflowSpecification
from polyaxon_schemas.utils import TaskType


class TestPolyaxonfileDeprecation(TestCase):

    def test_simple_file_framework_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/deprecated/simple_file_framework.yml'))
        spec = plxfile.specification
        spec.parse_data()
        assert spec.version == 1
        assert spec.logging is None
        assert spec.tags is None
        assert spec.build.dockerfile == 'Dockerfile'
        assert spec.run.cmd == 'video_prediction_train --model=DNA --num_masks=1'
        assert spec.environment is not None
        assert spec.environment.resources.gpu.to_dict() == {'requests': 1, 'limits': 1}
        assert spec.environment.outputs.to_dict() == {'jobs': [111], 'experiments': None}
        assert spec.framework is not None
        assert spec.is_experiment is True

    def test_deprecated_advanced_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/deprecated/advanced_file.yml'))
        spec = plxfile.specification
        spec.parse_data()
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.config.tensorflow.n_workers == 5
        assert spec.config.tensorflow.n_ps == 10

        # check properties for returning worker configs and resources
        assert spec.config.tensorflow.worker_resources == {}
        assert spec.config.tensorflow.ps_resources == {}

        cluster, is_distributed = spec.cluster_def

        assert TensorflowSpecification.get_worker_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        assert TensorflowSpecification.get_ps_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

    def test_deprecated_notebook_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/deprecated/notebook_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.parse_data()
        assert spec.version == 1
        assert spec.is_notebook
        assert spec.is_notebook is True
        assert spec.backend is None
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
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

    def test_deprecated_advanced_file_with_custom_configs_and_resources_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/deprecated/advanced_file_with_custom_configs_and_resources.yml'))
        spec = plxfile.specification
        spec.parse_data()
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        assert spec.config_map_refs == ['config_map1', 'config_map2']
        assert spec.config.tensorflow.n_workers == 5
        assert spec.config.tensorflow.n_ps == 10

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.config.tensorflow.default_worker_node_selector == {
            'foo': True
        }

        assert spec.config.tensorflow.worker_resources == {}
        assert spec.config.tensorflow.worker_affinities == {}
        assert isinstance(spec.config.tensorflow.worker_node_selectors[3], dict)
        assert spec.config.tensorflow.worker_node_selectors[3] == {
            'foo': False
        }
        assert isinstance(spec.config.tensorflow.worker_tolerations[4], list)
        assert spec.config.tensorflow.worker_tolerations[4] == [{
            'key': 'key',
            'operator': 'Exists',
            'effect': 'NoSchedule',
        }]

        assert isinstance(spec.config.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.config.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.config.tensorflow.default_ps_resources.cpu.limits == 4

        assert spec.config.tensorflow.ps_node_selectors == {}
        assert isinstance(spec.config.tensorflow.ps_tolerations[7], list)
        assert spec.config.tensorflow.ps_tolerations[7] == [{
            'operator': 'Exists'
        }]
        assert isinstance(spec.config.tensorflow.ps_affinities[7], dict)
        assert isinstance(spec.config.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.config.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.config.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.tensorflow.n_workers
        assert set([i['foo'] for i in worker_node_selectors.values()]) == {
            spec.config.tensorflow.default_worker_node_selector['foo'],
            spec.config.tensorflow.worker_node_selectors[3]['foo']}

        assert TensorflowSpecification.get_worker_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.config.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.config.tensorflow.default_ps_resources,
            spec.config.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 2 * 9, 'limits': 2 + 4 * 9},
            'memory': {'requests': 512, 'limits': 1024},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)
