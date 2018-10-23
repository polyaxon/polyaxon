# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.job import job


class TestJob(BaseCommandTestCase):

    @patch('polyaxon_client.api.job.JobApi.get_job')
    @patch('polyaxon_cli.managers.project.ProjectManager.is_initialized')
    @patch('polyaxon_cli.managers.job.JobManager.set_config')
    @patch('polyaxon_cli.cli.job.get_job_details')
    def test_get_job(self,
                     get_job_details,
                     set_config,
                     is_initialized,
                     get_job):
        self.runner.invoke(job, ['--project=admin/foo', '--job=1', 'get'])
        assert get_job.call_count == 1
        assert set_config.call_count == 1
        assert is_initialized.call_count == 1
        assert get_job_details.call_count == 1

    @patch('polyaxon_client.api.job.JobApi.update_job')
    def test_update_job(self, update_job):
        self.runner.invoke(job, ['update'])
        assert update_job.call_count == 0

        self.runner.invoke(job, ['--project=admin/foo',
                                 '--job=1',
                                 'update',
                                 '--description=foo'])
        assert update_job.call_count == 1

    @patch('polyaxon_client.api.job.JobApi.stop')
    def test_stop_job(self, stop):
        self.runner.invoke(job, ['stop'])
        assert stop.call_count == 0

        self.runner.invoke(job, ['--project=admin/foo',
                                 '--job=1',
                                 'stop',
                                 '-y'])
        assert stop.call_count == 1

    @patch('polyaxon_client.api.job.JobApi.get_statuses')
    def test_job_statuses(self, get_statuses):
        self.runner.invoke(job, ['--project=admin/foo', '--job=1', 'statuses'])
        assert get_statuses.call_count == 1

    @patch('polyaxon_client.api.job.JobApi.bookmark')
    def test_job_bookmark(self, bookmark):
        self.runner.invoke(job, ['--project=admin/foo', '--job=1', 'bookmark'])
        assert bookmark.call_count == 1

    @patch('polyaxon_client.api.job.JobApi.unbookmark')
    def test_job_unbookmark(self, unbookmark):
        self.runner.invoke(job, ['--project=admin/foo', '--job=1', 'unbookmark'])
        assert unbookmark.call_count == 1
