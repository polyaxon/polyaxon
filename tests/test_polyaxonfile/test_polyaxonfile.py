# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

import pytest

from flaky import flaky

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.ops.container import ContainerConfig
from polyaxon_schemas.ops.contexts import ContextsConfig
from polyaxon_schemas.ops.environments import EnvironmentConfig
from polyaxon_schemas.ops.parallel import (
    GridSearchConfig,
    HyperbandConfig,
    ParallelConfig,
    RandomSearchConfig,
)
from polyaxon_schemas.ops.parallel.early_stopping_policies import (
    MetricEarlyStoppingConfig,
)
from polyaxon_schemas.ops.parallel.matrix import (
    MatrixChoiceConfig,
    MatrixLinSpaceConfig,
)
from polyaxon_schemas.ops.termination import TerminationConfig
from polyaxon_schemas.polyaxonfile import PolyaxonFile
from polyaxon_schemas.specs import JobSpecification
from polyaxon_schemas.utils import TaskType


@pytest.mark.polyaxonfile_mark
class TestPolyaxonfileXXX(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/missing_version.yml"))

    def test_non_supported_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/non_supported_file.yml"))

    def test_non_exisiting_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/non_exisiting_file.yml"))

    def test_missing_kind_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath("tests/fixtures/plain/missing_kind.yml"))

    def test_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath("tests/fixtures/plain/simple_job.yml"))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags is None
        assert spec.params is None
        assert spec.container.image == "python-with-boto3"
        assert spec.container.command == "python download-s3-bucket"
        assert spec.environment is not None
        assert spec.resources.to_dict() == {
            "requests": {"nvidia.com/gpu": 1},
            "limits": {"nvidia.com/gpu": 1},
        }
        assert spec.is_job

    def test_passing_params_overrides_polyaxonfiles(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/simple_job.yml"),
            params={"foo": "bar", "value": 1.1},
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags is None
        assert spec.params == {"foo": "bar", "value": 1.1}
        assert spec.container.image == "python-with-boto3"
        assert spec.container.command == "python download-s3-bucket"
        assert spec.environment is not None
        assert spec.resources.to_dict() == {
            "requests": {"nvidia.com/gpu": 1},
            "limits": {"nvidia.com/gpu": 1},
        }
        assert spec.is_job

    def test_passing_wrong_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath("tests/fixtures/plain/simple_job.yml"), params="foo"
            )

    def test_passing_debug_ttl_overrides_polyaxonfiles(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/simple_job.yml"), debug_ttl=100
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.tags is None
        assert spec.container.image == "python-with-boto3"
        assert spec.container.command == ["/bin/bash", "-c"]
        assert spec.container.args == "sleep 100"
        assert spec.environment is not None
        assert spec.resources.to_dict() == {
            "requests": {"nvidia.com/gpu": 1},
            "limits": {"nvidia.com/gpu": 1},
        }
        assert spec.is_job is True

    def test_passing_wrong_debug_ttl_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath("tests/fixtures/plain/simple_job.yml"), debug_ttl="foo"
            )

    def test_passing_wrong_kind_with_debug_ttl_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath("tests/fixtures/plain/matrix_file.yml"), debug_ttl=120
            )

        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath(
                    "tests/fixtures/plain/tensorboard_with_custom_environment.yml"
                ),
                debug_ttl=120,
            )

        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(
                os.path.abspath("tests/fixtures/plain/non_existing_file.yml"),
                debug_ttl=120,
            )

    def test_job_file_with_contexts_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/job_file_with_contexts.yml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.log_level == "INFO"
        assert isinstance(spec.contexts, ContextsConfig)
        assert spec.auth_context.enable is True
        assert spec.shm_context.enable is True
        assert spec.docker_context.enable is True
        assert spec.outputs.enable is True
        assert spec.outputs.manage is True
        assert len(spec.artifacts) == 2
        assert spec.artifacts[0].to_dict() == {
            "name": "data1",
            "paths": ["path1", "path2"],
            "manage": True,
        }
        assert spec.artifacts[1].to_dict() == {"name": "data2", "manage": True}
        assert len(spec.secrets) == 1
        assert spec.secrets[0].to_dict() == {
            "name": "my_ssh_secret",
            "mount_path": "~/.ssh/id_rsa",
        }
        assert len(spec.config_maps) == 2
        assert spec.config_maps[0].to_dict() == {"name": "config_map1"}
        assert spec.config_maps[1].to_dict() == {
            "name": "config_map2",
            "items": ["item1", "item2"],
        }

    def test_job_file_with_termination_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/job_file_with_termination.yml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.termination, TerminationConfig)
        assert spec.max_retries == 5
        assert spec.timeout == 500
        assert spec.restart_policy == "never"
        assert spec.ttl == 400

    def test_job_file_with_environment_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/job_file_with_environment.yml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.node_selector == {"polyaxon.com": "core"}
        assert spec.resources.to_dict() == {
            "requests": {"cpu": 1, "memory": 200},
            "limits": {"cpu": 2, "memory": 200},
        }
        assert spec.affinity == {
            "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
        }
        assert spec.tolerations == [{"key": "key", "operator": "Exists"}]
        assert spec.labels == {"label_key1": "val1", "label_key2": "val2"}
        assert spec.annotations == {
            "annotation_key1": "val1",
            "annotation_key2": "val2",
        }
        assert spec.service_account == "new_sa"
        assert spec.image_pull_secrets == ["secret1", "secret2"]
        assert spec.env_vars == {"env_var_key1": "val1", "env_var_key2": "val2"}
        assert spec.security_context == {
            "runAsUser": 1000,
            "runAsGroup": 3000,
            "fsGroup": 5000,
        }
        assert spec.log_level == "DEBUG"

    def test_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath("tests/fixtures/plain/matrix_file.yml"))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.parallel, ParallelConfig)
        assert isinstance(spec.parallel.algorithm.matrix["lr"], MatrixLinSpaceConfig)
        assert isinstance(spec.parallel.algorithm.matrix["loss"], MatrixChoiceConfig)
        assert spec.parallel.algorithm.matrix["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert spec.parallel.algorithm.matrix["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert spec.parallel.algorithm.matrix["normal_rate"].to_dict() == {
            "kind": "normal",
            "value": {"loc": 0, "scale": 0.9},
        }
        assert spec.parallel.algorithm.matrix["dropout"].to_dict() == {
            "kind": "qloguniform",
            "value": {"high": 0.8, "low": 0, "q": 0.1},
        }
        assert spec.parallel.algorithm.matrix["activation"].to_dict() == {
            "kind": "pchoice",
            "value": [["relu", 0.1], ["sigmoid", 0.8]],
        }
        assert spec.parallel.algorithm.matrix["model"].to_dict() == {
            "kind": "choice",
            "value": ["CDNA", "DNA", "STP"],
        }
        assert spec.parallel.concurrency == 2
        assert spec.parallel_algorithm == HyperbandConfig.IDENTIFIER
        assert spec.parallel.early_stopping is None
        assert spec.parallel_early_stopping == []

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/matrix_file_with_int_float_types.yml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.parallel, ParallelConfig)
        assert isinstance(spec.parallel.algorithm.matrix["param1"], MatrixChoiceConfig)
        assert isinstance(spec.parallel.algorithm.matrix["param2"], MatrixChoiceConfig)
        assert spec.parallel.algorithm.matrix["param1"].to_dict() == {
            "kind": "choice",
            "value": [1, 2],
        }
        assert spec.parallel.algorithm.matrix["param2"].to_dict() == {
            "kind": "choice",
            "value": [3.3, 4.4],
        }
        assert spec.parallel.concurrency == 2
        assert spec.parallel_algorithm == GridSearchConfig.IDENTIFIER
        assert spec.parallel.early_stopping is None
        assert spec.parallel_early_stopping == []

    def test_matrix_early_stopping_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/matrix_file_early_stopping.yml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 0.6
        assert spec.is_job
        assert isinstance(spec.parallel, ParallelConfig)
        assert isinstance(spec.parallel.algorithm.matrix["lr"], MatrixLinSpaceConfig)
        assert isinstance(spec.parallel.algorithm.matrix["loss"], MatrixChoiceConfig)
        assert spec.parallel.algorithm.matrix["lr"].to_dict() == {
            "kind": "linspace",
            "value": {"start": 0.01, "stop": 0.1, "num": 5},
        }
        assert spec.parallel.algorithm.matrix["loss"].to_dict() == {
            "kind": "choice",
            "value": ["MeanSquaredError", "AbsoluteDifference"],
        }
        assert spec.parallel.concurrency == 2
        assert spec.parallel.algorithm.n_experiments == 300
        assert spec.parallel_algorithm == RandomSearchConfig.IDENTIFIER
        assert spec.parallel_early_stopping == spec.parallel.early_stopping
        assert len(spec.parallel_early_stopping) == 1
        assert isinstance(spec.parallel_early_stopping[0], MetricEarlyStoppingConfig)

    # def test_tf_passes(self):
    #     plxfile = PolyaxonFile(
    #         os.path.abspath("tests/fixtures/plain/distributed_tensorflow_file.yml")
    #     )
    #     spec = plxfile.specification
    #     spec.apply_context()
    #     assert spec.version == 1
    #     assert isinstance(spec.logging, LoggingConfig)
    #     assert spec.is_experiment
    #     assert isinstance(spec.environment, EnvironmentConfig)
    #     assert spec.environment.node_selector is None
    #     assert spec.master_node_selector is None
    #     assert spec.framework == ExperimentFramework.TENSORFLOW
    #     assert spec.config.tensorflow.n_workers == 5
    #     assert spec.config.tensorflow.n_ps == 10
    #
    #     assert spec.environment.tolerations is None
    #     assert spec.environment.node_selector is None
    #     assert isinstance(spec.environment.affinity, dict)
    #     assert spec.environment.resources == {
    #         "requests": {"cpu": 1},
    #         "limits": {"cpu": 2},
    #     }
    #
    #     assert spec.config.tensorflow.default_worker_node_selector is None
    #     assert spec.config.tensorflow.default_worker_affinity is None
    #     assert isinstance(spec.config.tensorflow.default_worker_tolerations, list)
    #     assert spec.config.tensorflow.default_worker_resources == {
    #         "requests": {"cpu": 3, "memory": "256Mi"},
    #         "limits": {"cpu": 3, "memory": "256Mi"},
    #     }
    #
    #     assert spec.config.tensorflow.worker_tolerations[2] == [{"operator": "Exists"}]
    #     assert spec.config.tensorflow.worker_resources[3] == {
    #         "requests": {"memory": "300Mi"},
    #         "limits": {"memory": "300Mi"},
    #     }
    #
    #     assert spec.config.tensorflow.default_ps_node_selector is None
    #     assert spec.config.tensorflow.default_ps_affinity is None
    #     assert isinstance(spec.config.tensorflow.default_ps_tolerations, list)
    #     assert spec.config.tensorflow.default_ps_resources == {
    #         "requests": {"cpu": 2},
    #         "limits": {"cpu": 4},
    #     }
    #
    #     assert spec.config.tensorflow.ps_resources[9] == {
    #         "requests": {"memory": "512Mi"},
    #         "limits": {"memory": "1024Mi"},
    #     }
    #
    #     # check that properties for return list of configs and resources is working
    #     cluster, is_distributed = spec.cluster_def
    #     worker_affinities = TensorflowSpecification.get_worker_affinities(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     worker_tolerations = TensorflowSpecification.get_worker_tolerations(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     worker_resources = TensorflowSpecification.get_worker_resources(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     assert worker_affinities == {}
    #     assert worker_node_selectors == {}
    #     assert len(worker_tolerations) == spec.config.tensorflow.n_workers
    #     assert len(worker_resources) == spec.config.tensorflow.n_workers
    #
    #     ps_tolerations = TensorflowSpecification.get_ps_tolerations(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     ps_affinities = TensorflowSpecification.get_ps_affinities(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     ps_resources = TensorflowSpecification.get_ps_resources(
    #         environment=spec.config.tensorflow,
    #         cluster=cluster,
    #         is_distributed=is_distributed,
    #     )
    #     assert ps_affinities == {}
    #     assert ps_node_selectors == {}
    #     assert len(ps_tolerations) == spec.config.tensorflow.n_ps
    #     assert len(ps_resources) == spec.config.tensorflow.n_ps
    #
    #     assert spec.cluster_def == (
    #         {TaskType.MASTER: 1, TaskType.WORKER: 5, TaskType.PS: 10},
    #         True,
    #     )
    #
    #     def test_distributed_tensorflow_passes_with_node_selectors(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/distributed_tensorflow_with_node_selectors_file.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.environment.node_selector == {
    #             "polyaxon.com": "node_for_master_task"
    #         }
    #         assert spec.master_node_selector == {"polyaxon.com": "node_for_master_task"}
    #         assert spec.framework == ExperimentFramework.TENSORFLOW
    #         assert spec.config.tensorflow.n_workers == 5
    #         assert spec.config.tensorflow.n_ps == 10
    #
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.tensorflow.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert spec.config.tensorflow.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         assert spec.config.tensorflow.default_ps_resources == {
    #             "requests": {"cpu": 2},
    #             "limits": {"cpu": 4},
    #         }
    #
    #         assert spec.config.tensorflow.ps_resources[9] == {
    #             "requests": {"memory": "512Mi"},
    #             "limits": {"memory": "1024Mi"},
    #         }
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = TensorflowSpecification.get_worker_resources(
    #             environment=spec.config.tensorflow,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_resources) == spec.config.tensorflow.n_workers
    #
    #         ps_resources = TensorflowSpecification.get_ps_resources(
    #             environment=spec.config.tensorflow,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(ps_resources) == spec.config.tensorflow.n_ps
    #
    #         assert spec.cluster_def == (
    #             {TaskType.MASTER: 1, TaskType.WORKER: 5, TaskType.PS: 10},
    #             True,
    #         )
    #
    #         assert spec.config.tensorflow.default_worker.node_selector == {
    #             "polyaxon.com": "node_for_worker_tasks"
    #         }
    #         assert spec.config.tensorflow.worker_node_selectors[2] == {
    #             "polyaxon.com": "node_for_worker_task_2"
    #         }
    #
    #         assert spec.config.tensorflow.default_ps.node_selector == {
    #             "polyaxon.com": "node_for_ps_tasks"
    #         }
    #         assert spec.config.tensorflow.ps_node_selectors[2] == {
    #             "polyaxon.com": "node_for_ps_task_2"
    #         }
    #
    #         worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
    #             environment=spec.config.tensorflow,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_node_selectors) == spec.config.tensorflow.n_workers
    #         assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
    #             tuple(spec.config.tensorflow.default_worker.node_selector.items()),
    #             tuple(spec.config.tensorflow.worker_node_selectors[2].items()),
    #         }
    #
    #         ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
    #             environment=spec.config.tensorflow,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(ps_node_selectors) == spec.config.tensorflow.n_ps
    #         assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
    #             tuple(spec.config.tensorflow.default_ps.node_selector.items()),
    #             tuple(spec.config.tensorflow.ps_node_selectors[2].items()),
    #         }
    #
    #     def test_distributed_horovod_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath("tests/fixtures/plain/distributed_horovod_file.yml")
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.framework == ExperimentFramework.HOROVOD
    #         assert spec.config.horovod.n_workers == 5
    #
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.horovod.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert spec.config.horovod.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         assert isinstance(spec.environment.affinity, dict)
    #         assert spec.config.horovod.worker_affinities == {}
    #
    #         assert spec.environment.tolerations is None
    #         assert isinstance(spec.config.horovod.default_worker_tolerations, list)
    #         assert isinstance(spec.config.horovod.worker_tolerations[2], list)
    #         assert spec.config.horovod.worker_tolerations[2] == [{"operator": "Exists"}]
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = HorovodSpecification.get_worker_resources(
    #             environment=spec.config.horovod,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
    #             environment=spec.config.horovod,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_affinities = HorovodSpecification.get_worker_affinities(
    #             environment=spec.config.horovod,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_tolerations = HorovodSpecification.get_worker_tolerations(
    #             environment=spec.config.horovod,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #
    #         assert worker_node_selectors == {}
    #         assert worker_affinities == {}
    #         assert len(worker_tolerations) == spec.config.horovod.n_workers
    #         assert len(worker_resources) == spec.config.horovod.n_workers
    #
    #         assert spec.cluster_def == ({TaskType.MASTER: 1, TaskType.WORKER: 5}, True)
    #
    #     def test_distributed_horovod_with_node_selectors_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/distributed_horovod_with_node_selectors_file.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.environment.node_selector == {
    #             "polyaxon.com": "node_for_master_task"
    #         }
    #         assert spec.master_node_selector == {"polyaxon.com": "node_for_master_task"}
    #         assert spec.framework == ExperimentFramework.HOROVOD
    #         assert spec.config.horovod.n_workers == 5
    #
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.horovod.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert spec.config.horovod.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = HorovodSpecification.get_worker_resources(
    #             environment=spec.config.horovod,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_resources) == spec.config.horovod.n_workers
    #
    #         assert spec.cluster_def == ({TaskType.MASTER: 1, TaskType.WORKER: 5}, True)
    #
    #         assert spec.config.horovod.default_worker.node_selector == {
    #             "polyaxon.com": "node_for_worker_tasks"
    #         }
    #         assert spec.config.horovod.worker_node_selectors[2] == {
    #             "polyaxon.com": "node_for_worker_task_2"
    #         }
    #
    #         worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
    #             environment=spec.config.horovod,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_node_selectors) == spec.config.horovod.n_workers
    #         assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
    #             tuple(spec.config.horovod.default_worker.node_selector.items()),
    #             tuple(spec.config.horovod.worker_node_selectors[2].items()),
    #         }
    #
    #     def test_distributed_pytorch_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath("tests/fixtures/plain/distributed_pytorch_file.yml")
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.framework == ExperimentFramework.PYTORCH
    #         assert spec.config.pytorch.n_workers == 5
    #
    #         assert spec.environment.node_selector is None
    #         assert spec.environment.tolerations is None
    #         assert isinstance(spec.environment.affinity, dict)
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.pytorch.default_worker_node_selector is None
    #         assert spec.config.pytorch.default_worker_affinity is None
    #         assert isinstance(spec.config.pytorch.default_worker_tolerations, list)
    #         assert isinstance(spec.config.pytorch.default_worker_tolerations[0], dict)
    #         assert spec.config.pytorch.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert spec.config.pytorch.worker_tolerations[2] == [{"operator": "Exists"}]
    #         assert spec.config.pytorch.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = PytorchSpecification.get_worker_resources(
    #             environment=spec.config.pytorch,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_tolerations = PytorchSpecification.get_worker_tolerations(
    #             environment=spec.config.pytorch,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
    #             environment=spec.config.pytorch,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_affinities = PytorchSpecification.get_worker_affinities(
    #             environment=spec.config.pytorch,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert worker_node_selectors == {}
    #         assert worker_affinities == {}
    #         assert len(worker_tolerations) == spec.config.pytorch.n_workers
    #         assert len(worker_resources) == spec.config.pytorch.n_workers
    #
    #         assert spec.cluster_def == ({TaskType.MASTER: 1, TaskType.WORKER: 5}, True)
    #
    #     def test_distributed_pytorch_with_node_selectors_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/distributed_pytorch_with_node_selectors_file.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.environment.node_selector == {
    #             "polyaxon.com": "node_for_master_task"
    #         }
    #         assert spec.master_node_selector == {"polyaxon.com": "node_for_master_task"}
    #         assert spec.framework == ExperimentFramework.PYTORCH
    #         assert spec.config.pytorch.n_workers == 5
    #
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.pytorch.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert spec.config.pytorch.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = PytorchSpecification.get_worker_resources(
    #             environment=spec.config.pytorch,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_resources) == spec.config.pytorch.n_workers
    #
    #         assert spec.cluster_def == ({TaskType.MASTER: 1, TaskType.WORKER: 5}, True)
    #
    #         assert spec.config.pytorch.default_worker.node_selector == {
    #             "polyaxon.com": "node_for_worker_tasks"
    #         }
    #         assert spec.config.pytorch.worker_node_selectors[2] == {
    #             "polyaxon.com": "node_for_worker_task_2"
    #         }
    #
    #         worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
    #             environment=spec.config.pytorch,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_node_selectors) == spec.config.pytorch.n_workers
    #         assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
    #             tuple(spec.config.pytorch.default_worker.node_selector.items()),
    #             tuple(spec.config.pytorch.worker_node_selectors[2].items()),
    #         }
    #
    #     def test_distributed_mpi_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath("tests/fixtures/plain/distributed_mpi_file.yml")
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.framework == ExperimentFramework.TENSORFLOW
    #         assert spec.backend == ExperimentBackend.MPI
    #         assert spec.config.mpi.n_workers == 8
    #
    #         assert spec.environment.node_selector is None
    #         assert spec.environment.tolerations is None
    #         assert spec.environment.affinity is None
    #         assert spec.environment.resources is None
    #
    #         assert spec.config.mpi.default_worker_node_selector is None
    #         assert spec.config.mpi.default_worker_affinity is None
    #         assert isinstance(spec.config.mpi.default_worker_tolerations, list)
    #         assert isinstance(spec.config.mpi.default_worker_tolerations[0], dict)
    #         assert spec.config.mpi.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi", "gpu": 4},
    #             "limits": {"cpu": 3, "memory": "256Mi", "gpu": 4},
    #         }
    #
    #         assert spec.config.mpi.worker_tolerations == {}
    #         assert spec.config.mpi.worker_resources == {}
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = PytorchSpecification.get_worker_resources(
    #             environment=spec.config.mpi, cluster=cluster, is_distributed=is_distributed
    #         )
    #         worker_tolerations = PytorchSpecification.get_worker_tolerations(
    #             environment=spec.config.mpi, cluster=cluster, is_distributed=is_distributed
    #         )
    #         worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
    #             environment=spec.config.mpi, cluster=cluster, is_distributed=is_distributed
    #         )
    #         worker_affinities = PytorchSpecification.get_worker_affinities(
    #             environment=spec.config.mpi, cluster=cluster, is_distributed=is_distributed
    #         )
    #         assert worker_node_selectors == {}
    #         assert worker_affinities == {}
    #         assert len(worker_tolerations) == spec.config.mpi.n_workers
    #         assert len(worker_resources) == spec.config.mpi.n_workers
    #
    #         assert spec.cluster_def == ({TaskType.WORKER: 8}, True)
    #
    #     def test_distributed_mpi_with_node_selectors_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/distributed_mpi_with_node_selectors_file.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert spec.framework == ExperimentFramework.PYTORCH
    #         assert spec.backend == ExperimentBackend.MPI
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.environment.node_selector is None
    #         assert spec.master_node_selector is None
    #         assert spec.config.mpi.n_workers == 4
    #
    #         assert spec.environment.resources is None
    #         assert spec.config.mpi.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi", "gpu": 2},
    #             "limits": {"cpu": 3, "memory": "256Mi", "gpu": 2},
    #         }
    #
    #         assert spec.config.mpi.worker_resources == {}
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = PytorchSpecification.get_worker_resources(
    #             environment=spec.config.mpi, cluster=cluster, is_distributed=is_distributed
    #         )
    #         assert len(worker_resources) == spec.config.mpi.n_workers
    #
    #         assert spec.cluster_def == ({TaskType.WORKER: 4}, True)
    #
    #         assert spec.config.mpi.default_worker.node_selector == {
    #             "polyaxon.com": "node_for_worker_tasks"
    #         }
    #
    #         worker_node_selectors = MPISpecification.get_worker_node_selectors(
    #             environment=spec.config.mpi, cluster=cluster, is_distributed=is_distributed
    #         )
    #         assert len(worker_node_selectors) == spec.config.mpi.n_workers
    #         assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
    #             tuple(spec.config.mpi.default_worker.node_selector.items())
    #         }
    #
    #     def test_distributed_mxnet_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath("tests/fixtures/plain/distributed_mxnet_file.yml")
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.framework == ExperimentFramework.MXNET
    #         assert spec.config.mxnet.n_workers == 5
    #         assert spec.config.mxnet.n_ps == 10
    #
    #         assert spec.environment.node_selector is None
    #         assert spec.environment.tolerations is None
    #         assert isinstance(spec.environment.affinity, dict)
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.mxnet.default_worker_node_selector is None
    #         assert spec.config.mxnet.default_worker_affinity is None
    #         assert isinstance(spec.config.mxnet.default_worker_tolerations, list)
    #         assert spec.config.mxnet.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert isinstance(spec.config.mxnet.worker_tolerations[2], list)
    #         assert spec.config.mxnet.worker_tolerations[2] == [{"operator": "Exists"}]
    #         assert spec.config.mxnet.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         assert spec.config.mxnet.default_ps_node_selector is None
    #         assert spec.config.mxnet.default_ps_affinity is None
    #         assert isinstance(spec.config.mxnet.default_ps_tolerations, list)
    #         assert spec.config.mxnet.default_ps_resources == {
    #             "requests": {"cpu": 2},
    #             "limits": {"cpu": 4},
    #         }
    #
    #         assert spec.config.mxnet.ps_resources[9] == {
    #             "requests": {"memory": "512Mi"},
    #             "limits": {"memory": "1024Mi"},
    #         }
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = MXNetSpecification.get_worker_resources(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_affinities = MXNetSpecification.get_worker_affinities(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         worker_tolerations = MXNetSpecification.get_worker_tolerations(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert worker_node_selectors == {}
    #         assert worker_affinities == {}
    #         assert len(worker_tolerations) == spec.config.mxnet.n_workers
    #         assert len(worker_resources) == spec.config.mxnet.n_workers
    #
    #         ps_resources = MXNetSpecification.get_ps_resources(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         ps_affinities = MXNetSpecification.get_ps_affinities(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         ps_tolerations = MXNetSpecification.get_ps_tolerations(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert ps_node_selectors == {}
    #         assert ps_affinities == {}
    #         assert len(ps_tolerations) == spec.config.mxnet.n_ps
    #         assert len(ps_resources) == spec.config.mxnet.n_ps
    #
    #         assert spec.cluster_def == (
    #             {TaskType.MASTER: 1, TaskType.WORKER: 5, TaskType.SERVER: 10},
    #             True,
    #         )
    #
    #     def test_distributed_mxnet_with_node_selectors_passes(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/distributed_mxnet_with_node_selectors_file.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_experiment
    #         assert isinstance(spec.logging, LoggingConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         assert spec.environment.node_selector == {
    #             "polyaxon.com": "node_for_master_task"
    #         }
    #         assert spec.master_node_selector == {"polyaxon.com": "node_for_master_task"}
    #         assert spec.framework == ExperimentFramework.MXNET
    #         assert spec.config.mxnet.n_workers == 5
    #         assert spec.config.mxnet.n_ps == 10
    #
    #         assert spec.environment.resources == {
    #             "requests": {"cpu": 1},
    #             "limits": {"cpu": 2},
    #         }
    #
    #         assert spec.config.mxnet.default_worker_resources == {
    #             "requests": {"cpu": 3, "memory": "256Mi"},
    #             "limits": {"cpu": 3, "memory": "256Mi"},
    #         }
    #
    #         assert spec.config.mxnet.worker_resources[3] == {
    #             "requests": {"memory": "300Mi"},
    #             "limits": {"memory": "300Mi"},
    #         }
    #
    #         assert spec.config.mxnet.default_ps_resources == {
    #             "requests": {"cpu": 2},
    #             "limits": {"cpu": 4},
    #         }
    #
    #         assert spec.config.mxnet.ps_resources[9] == {
    #             "requests": {"memory": "512Mi"},
    #             "limits": {"memory": "1024Mi"},
    #         }
    #
    #         # check that properties for return list of configs and resources is working
    #         cluster, is_distributed = spec.cluster_def
    #         worker_resources = MXNetSpecification.get_worker_resources(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_resources) == spec.config.mxnet.n_workers
    #
    #         ps_resources = MXNetSpecification.get_ps_resources(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(ps_resources) == spec.config.mxnet.n_ps
    #
    #         assert spec.cluster_def == (
    #             {TaskType.MASTER: 1, TaskType.WORKER: 5, TaskType.SERVER: 10},
    #             True,
    #         )
    #
    #         assert spec.config.mxnet.default_worker.node_selector == {
    #             "polyaxon.com": "node_for_worker_tasks"
    #         }
    #         assert spec.config.mxnet.worker_node_selectors[2] == {
    #             "polyaxon.com": "node_for_worker_task_2"
    #         }
    #
    #         assert spec.config.mxnet.default_ps.node_selector == {
    #             "polyaxon.com": "node_for_ps_tasks"
    #         }
    #         assert spec.config.mxnet.ps_node_selectors[2] == {
    #             "polyaxon.com": "node_for_ps_task_2"
    #         }
    #
    #         worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(worker_node_selectors) == spec.config.mxnet.n_workers
    #         assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
    #             tuple(spec.config.mxnet.default_worker.node_selector.items()),
    #             tuple(spec.config.mxnet.worker_node_selectors[2].items()),
    #         }
    #
    #         ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
    #             environment=spec.config.mxnet,
    #             cluster=cluster,
    #             is_distributed=is_distributed,
    #         )
    #         assert len(ps_node_selectors) == spec.config.mxnet.n_ps
    #         assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
    #             tuple(spec.config.mxnet.default_ps.node_selector.items()),
    #             tuple(spec.config.mxnet.ps_node_selectors[2].items()),
    #         }
    #
    #     def test_notebook_job_with_node_selectors(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath("tests/fixtures/plain/notebook_with_custom_environment.yml")
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_notebook
    #         assert spec.is_notebook is True
    #         assert spec.backend is None
    #         assert spec.logging is None
    #         assert sorted(spec.tags) == sorted(["foo", "bar"])
    #         assert isinstance(spec.build, BuildConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         artifact_refs = [r.to_light_dict()["name"] for r in spec.artifact_refs]
    #         assert len(artifact_refs) == 3
    #         assert set(artifact_refs) == {"data1", "data2", "outputs1"}
    #         assert [r.to_light_dict() for r in spec.secret_refs] == [
    #             {"name": "secret1"},
    #             {"name": "secret2"},
    #         ]
    #         assert [r.to_light_dict() for r in spec.config_map_refs] == [
    #             {"name": "config_map1"},
    #             {"name": "config_map2"},
    #         ]
    #
    #         node_selector = {"polyaxon.com": "node_for_notebook_jobs"}
    #         assert spec.environment.node_selector == node_selector
    #         assert spec.node_selector == node_selector
    #
    #         resources = {
    #             "requests": {"cpu": 1, "memory": "200Mi"},
    #             "limits": {"cpu": 2, "memory": "200Mi"},
    #         }
    #         assert spec.environment.resources == resources
    #         assert spec.resources == resources
    #
    #         affinity = {
    #             "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
    #         }
    #         assert spec.environment.affinity == affinity
    #         assert spec.affinity == affinity
    #
    #         tolerations = [{"key": "key", "operator": "Exists"}]
    #
    #         assert spec.environment.tolerations == tolerations
    #         assert spec.tolerations == tolerations
    #
    #     def test_jupyter_lab_job_with_node_selectors(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/jupyterlab_with_custom_environment.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_notebook
    #         assert spec.is_notebook is True
    #         assert spec.backend == "lab"
    #         assert spec.logging is None
    #         assert sorted(spec.tags) == sorted(["foo", "bar"])
    #         assert isinstance(spec.build, BuildConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         artifact_refs = [r.to_light_dict()["name"] for r in spec.artifact_refs]
    #         assert len(artifact_refs) == 3
    #         assert set(artifact_refs) == {"data1", "data2", "outputs1"}
    #         assert [r.to_light_dict() for r in spec.secret_refs] == [
    #             {"name": "secret1"},
    #             {"name": "secret2"},
    #         ]
    #         assert [r.to_light_dict() for r in spec.config_map_refs] == [
    #             {"name": "config_map1"},
    #             {"name": "config_map2"},
    #         ]
    #
    #         node_selector = {"polyaxon.com": "node_for_notebook_jobs"}
    #         labels = {"key1": "value1", "key2": "value2"}
    #         annotations = {"anno1": "value1"}
    #
    #         assert spec.environment.node_selector == node_selector
    #         assert spec.node_selector == node_selector
    #         assert spec.environment.labels == labels
    #         assert spec.labels == labels
    #         assert spec.environment.annotations == annotations
    #         assert spec.annotations == annotations
    #
    #         resources = {
    #             "requests": {"cpu": 1, "memory": "200Mi"},
    #             "limits": {"cpu": 2, "memory": "200Mi"},
    #         }
    #         assert spec.environment.resources == resources
    #         assert spec.resources == resources
    #
    #         affinity = {
    #             "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
    #         }
    #         assert spec.environment.affinity == affinity
    #         assert spec.affinity == affinity
    #
    #         tolerations = [{"key": "key", "operator": "Exists"}]
    #
    #         assert spec.environment.tolerations == tolerations
    #         assert spec.tolerations == tolerations
    #
    #     def test_tensorboard_job_with_node_selectors(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath(
    #                 "tests/fixtures/plain/tensorboard_with_custom_environment.yml"
    #             )
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_tensorboard
    #         assert spec.is_tensorboard is True
    #         assert spec.logging is None
    #         assert sorted(spec.tags) == sorted(["foo", "bar"])
    #         assert isinstance(spec.build, BuildConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #
    #         node_selector = {"polyaxon.com": "node_for_tensorboard_jobs"}
    #         assert spec.environment.node_selector == node_selector
    #         assert spec.node_selector == node_selector
    #
    #         resources = {
    #             "requests": {"cpu": 1, "memory": "200Mi"},
    #             "limits": {"cpu": 2, "memory": "200Mi"},
    #         }
    #         assert spec.environment.resources == resources
    #         assert spec.resources == resources
    #
    #         affinity = {
    #             "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
    #         }
    #         assert spec.environment.affinity == affinity
    #         assert spec.affinity == affinity
    #
    #         tolerations = [{"key": "key", "operator": "Exists"}]
    #
    #         assert spec.environment.tolerations == tolerations
    #         assert spec.tolerations == tolerations
    #
    #     def test_run_job_with_node_selectors(self):
    #         plxfile = PolyaxonFile(
    #             os.path.abspath("tests/fixtures/plain/run_with_custom_environment.yml")
    #         )
    #         spec = plxfile.specification
    #         spec.apply_context()
    #         assert spec.version == 1
    #         assert spec.is_job
    #         assert sorted(spec.tags) == sorted(["foo", "bar"])
    #         assert spec.logging is None
    #         assert isinstance(spec.build, BuildConfig)
    #         assert isinstance(spec.run, RunConfig)
    #         assert isinstance(spec.environment, EnvironmentConfig)
    #         artifact_refs = [r.to_light_dict()["name"] for r in spec.artifact_refs]
    #         assert len(artifact_refs) == 3
    #         assert set(artifact_refs) == {"data1", "data2", "outputs1"}
    #         assert [r.to_light_dict() for r in spec.secret_refs] == [
    #             {"name": "secret1"},
    #             {"name": "secret2"},
    #         ]
    #         assert [r.to_light_dict() for r in spec.config_map_refs] == [
    #             {"name": "config_map1"},
    #             {"name": "config_map2"},
    #         ]
    #
    #         node_selector = {"polyaxon.com": "node_for_jobs"}
    #         assert spec.environment.node_selector == node_selector
    #         assert spec.node_selector == node_selector
    #
    #         resources = {
    #             "requests": {"cpu": 1, "memory": "200Mi"},
    #             "limits": {"cpu": 2, "memory": "200Mi"},
    #         }
    #         assert spec.environment.resources == resources
    #         assert spec.resources == resources
    #
    #         affinity = {
    #             "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
    #         }
    #         assert spec.environment.affinity == affinity
    #         assert spec.affinity == affinity
    #
    #         tolerations = [{"key": "key", "operator": "Exists"}]
    #
    #         assert spec.environment.tolerations == tolerations
    #         assert spec.tolerations == tolerations
    #
    #
    def test_specification_with_quotes(self):
        plxfile = PolyaxonFile(
            os.path.abspath("tests/fixtures/plain/polyaxonfile_with_quotes.yaml")
        )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.container.image == "continuumio/miniconda3"
        assert spec.container.command == ["python"]
        assert spec.container.args == ["-c \"print('Tweet tweet')\""]
        spec = JobSpecification(spec.raw_data)
        spec.apply_context()
        assert spec.container.image == "continuumio/miniconda3"
        assert spec.container.command == ["python"]
        assert spec.container.args == ["-c \"print('Tweet tweet')\""]
