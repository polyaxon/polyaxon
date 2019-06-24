# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os
import uuid

from tests.utils import TestEnvVarsCase

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking.experiment import Experiment


class TestExperimentTracking(TestEnvVarsCase):
    def setUp(self):
        super(TestExperimentTracking, self).setUp()
        settings.IS_MANAGED = True

    def test_cluster_def_checks_is_managed(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            Experiment.get_cluster_def()

    def test_empty_cluster_def(self):
        self.check_empty_value('POLYAXON_CLUSTER', Experiment.get_cluster_def)

    def test_non_dict_cluster_def(self):
        self.check_non_dict_value('POLYAXON_CLUSTER', Experiment.get_cluster_def)

    def test_dict_cluster_def(self):
        cluster_def = {
            "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
            "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                       "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
            "ps": ["plxjob-ps3-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        }
        self.check_valid_dict_value('POLYAXON_CLUSTER', Experiment.get_cluster_def, cluster_def)

    def test_params_checks_is_managed(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            Experiment.get_params()

    def test_empty_params(self):
        self.check_empty_value('POLYAXON_PARAMS', Experiment.get_params)

    def test_non_dict_params(self):
        self.check_non_dict_value('POLYAXON_PARAMS', Experiment.get_params)

    def test_dict_params(self):
        params = {
            "foo": "bar"
        }
        self.check_valid_dict_value('POLYAXON_PARAMS',
                                    Experiment.get_params,
                                    params)

    def test_experiment_info_checks_is_managed(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            Experiment.get_experiment_info()

    def test_empty_experiment_info(self):
        self.check_empty_value('POLYAXON_EXPERIMENT_INFO', Experiment.get_experiment_info)

    def test_non_dict_experiment_info(self):
        self.check_non_dict_value('POLYAXON_EXPERIMENT_INFO', Experiment.get_experiment_info)

    def test_dict_experiment_info(self):
        experiment_info = {
            "project_name": "project_bar",
            "experiment_group_name": None,
            "experiment_name": "project_bar.1",
            "project_uuid": uuid.uuid4().hex,
            "experiment_group_uuid": None,
            "experiment_uuid": uuid.uuid4().hex,
        }
        self.check_valid_dict_value('POLYAXON_EXPERIMENT_INFO',
                                    Experiment.get_experiment_info,
                                    experiment_info)

    def test_task_info_checks_is_managed(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            Experiment.get_task_info()

    def test_empty_task_info(self):
        self.check_empty_value('POLYAXON_TASK_INFO', Experiment.get_task_info)

    def test_non_dict_task_info(self):
        self.check_non_dict_value('POLYAXON_TASK_INFO', Experiment.get_task_info)

    def test_dict_task_info(self):
        task_info = {"type": 'master', "index": 0}
        self.check_valid_dict_value('POLYAXON_TASK_INFO',
                                    Experiment.get_task_info,
                                    task_info)

    def test_tf_config_checks_is_managed(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            Experiment.get_tf_config()

    def test_empty_tf_config(self):
        os.environ['POLYAXON_RUN_OUTPUTS_PATH'] = 'path'
        assert Experiment.get_tf_config() == {
            'cluster': None,
            'task': None,
            'model_dir': 'path',
            'environment': 'cloud'
        }

    def test_non_dict_tf_config(self):
        os.environ['POLYAXON_RUN_OUTPUTS_PATH'] = 'path'
        os.environ['POLYAXON_CLUSTER'] = 'value'
        os.environ['POLYAXON_TASK_INFO'] = 'value'
        assert Experiment.get_tf_config() == {
            'cluster': None,
            'task': None,
            'model_dir': 'path',
            'environment': 'cloud'
        }

    def test_dict_tf_config(self):
        cluster_def = {
            "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
            "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                       "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
            "ps": ["plxjob-ps3-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        }
        task_info = {"type": 'master', "index": 0}
        os.environ['POLYAXON_CLUSTER'] = json.dumps(cluster_def)
        os.environ['POLYAXON_TASK_INFO'] = json.dumps(task_info)
        os.environ['POLYAXON_RUN_OUTPUTS_PATH'] = 'path'
        assert Experiment.get_tf_config() == {
            'cluster': cluster_def,
            'task': {"type": 'master', "index": 0},
            'model_dir': 'path',
            'environment': 'cloud'
        }
