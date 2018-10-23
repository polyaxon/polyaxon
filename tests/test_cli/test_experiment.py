# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.experiment import experiment


class TestExperiment(BaseCommandTestCase):

    @patch('polyaxon_client.api.experiment.ExperimentApi.get_experiment')
    @patch('polyaxon_cli.managers.project.ProjectManager.is_initialized')
    @patch('polyaxon_cli.managers.experiment.ExperimentManager.set_config')
    @patch('polyaxon_cli.cli.experiment.get_experiment_details')
    def test_get_experiment(self, get_experiment_details,
                            set_config,
                            is_initialized,
                            get_experiment):
        self.runner.invoke(experiment, ['--project=admin/foo', '--experiment=1', 'get'])
        assert get_experiment.call_count == 1
        assert set_config.call_count == 1
        assert is_initialized.call_count == 1
        assert get_experiment_details.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.update_experiment')
    def test_update_experiment(self, update_experiment):
        self.runner.invoke(experiment, ['update'])
        assert update_experiment.call_count == 0

        self.runner.invoke(experiment, ['--project=admin/foo',
                                        '--experiment=1',
                                        'update',
                                        '--description=foo'])
        assert update_experiment.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.stop')
    def test_stop_experiment(self, stop):
        self.runner.invoke(experiment, ['stop'])
        assert stop.call_count == 0

        self.runner.invoke(experiment, ['--project=admin/foo',
                                        '--experiment=1',
                                        'stop',
                                        '-y'])
        assert stop.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.restart')
    def test_restart_experiment(self, restart):
        self.runner.invoke(experiment, ['restart'])
        assert restart.call_count == 0

        self.runner.invoke(experiment, ['--project=admin/foo',
                                        '--experiment=1',
                                        'restart'])
        assert restart.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.copy')
    def test_copy_experiment(self, copy):
        self.runner.invoke(experiment, ['restart'])
        assert copy.call_count == 0

        self.runner.invoke(experiment, ['--project=admin/foo',
                                        '--experiment=1',
                                        'restart',
                                        '-c'])
        assert copy.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.resume')
    def test_resume_experiment(self, resume):
        self.runner.invoke(experiment, ['resume'])
        assert resume.call_count == 0

        self.runner.invoke(experiment, ['--project=admin/foo',
                                        '--experiment=1',
                                        'resume'])
        assert resume.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.get_statuses')
    def test_experiment_statuses(self, get_statuses):
        self.runner.invoke(experiment, ['--project=admin/foo', '--experiment=1', 'statuses'])
        assert get_statuses.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.list_jobs')
    def test_experiment_jobs(self, list_jobs):
        self.runner.invoke(experiment, ['--project=admin/foo', '--experiment=1', 'jobs'])
        assert list_jobs.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.download_outputs')
    def test_experiment_download_repo(self, download_outputs):
        self.runner.invoke(experiment, ['--project=admin/foo', '--experiment=1', 'outputs'])
        assert download_outputs.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.bookmark')
    def test_experiment_bookmark(self, bookmark):
        self.runner.invoke(experiment, ['--project=admin/foo', '--experiment=1', 'bookmark'])
        assert bookmark.call_count == 1

    @patch('polyaxon_client.api.experiment.ExperimentApi.unbookmark')
    def test_experiment_unbookmark(self, unbookmark):
        self.runner.invoke(experiment, ['--project=admin/foo', '--experiment=1', 'unbookmark'])
        assert unbookmark.call_count == 1
