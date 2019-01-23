# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.experiment_group import group


class TestExperimentGroup(BaseCommandTestCase):

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.get_experiment_group')
    @patch('polyaxon_cli.managers.project.ProjectManager.is_initialized')
    @patch('polyaxon_cli.managers.experiment_group.GroupManager.set_config')
    @patch('polyaxon_cli.cli.experiment_group.get_group_details')
    def test_get_group(self,
                       get_group_details,
                       set_config,
                       is_initialized,
                       get_experiment_group):
        self.runner.invoke(group, ['--project=admin/foo', '--group=1', 'get'])
        assert get_experiment_group.call_count == 1
        assert set_config.call_count == 1
        assert is_initialized.call_count == 1
        assert get_group_details.call_count == 1

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.update_experiment_group')
    def test_update_group(self, update_experiment_group):
        self.runner.invoke(group, ['update'])
        assert update_experiment_group.call_count == 0

        self.runner.invoke(group, ['--project=admin/foo',
                                   '--group=1',
                                   'update',
                                   '--description=foo'])
        assert update_experiment_group.call_count == 1

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.stop')
    def test_stop_group(self, stop):
        self.runner.invoke(group, ['stop'])
        assert stop.call_count == 0

        self.runner.invoke(group, ['--project=admin/foo',
                                   '--group=1',
                                   'stop',
                                   '-y'])
        assert stop.call_count == 1

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.get_statuses')
    def test_group_statuses(self, get_statuses):
        self.runner.invoke(group, ['--project=admin/foo', '--group=1', 'statuses'])
        assert get_statuses.call_count == 1

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.list_experiments')
    def test_group_experiment(self, list_experiments):
        self.runner.invoke(group, ['--project=admin/foo', '--group=1', 'experiments'])
        assert list_experiments.call_count == 1

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.bookmark')
    def test_group_bookmark(self, bookmark):
        self.runner.invoke(group, ['--project=admin/foo', '--group=1', 'bookmark'])
        assert bookmark.call_count == 1

    @patch('polyaxon_client.api.experiment_group.ExperimentGroupApi.unbookmark')
    def test_group_unbookmark(self, unbookmark):
        self.runner.invoke(group, ['--project=admin/foo', '--group=1', 'unbookmark'])
        assert unbookmark.call_count == 1
