# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.build import build


class TestBuild(BaseCommandTestCase):

    @patch('polyaxon_client.api.build_job.BuildJobApi.get_build')
    @patch('polyaxon_cli.managers.project.ProjectManager.is_initialized')
    @patch('polyaxon_cli.managers.build_job.BuildJobManager.set_config')
    @patch('polyaxon_cli.cli.build.get_build_details')
    def test_get_build(self,
                       get_build_details,
                       set_config,
                       is_initialized,
                       get_build):
        self.runner.invoke(build, ['--project=admin/foo', '--build=1', 'get'])
        assert get_build.call_count == 1
        assert set_config.call_count == 1
        assert is_initialized.call_count == 1
        assert get_build_details.call_count == 1

    @patch('polyaxon_client.api.build_job.BuildJobApi.update_build')
    def test_update_build(self, update_build):
        self.runner.invoke(build, ['update'])
        assert update_build.call_count == 0

        self.runner.invoke(build, ['--project=admin/foo',
                                   '--build=1',
                                   'update',
                                   '--description=foo'])
        assert update_build.call_count == 1

    @patch('polyaxon_client.api.build_job.BuildJobApi.stop')
    def test_stop_build(self, stop):
        self.runner.invoke(build, ['stop'])
        assert stop.call_count == 0

        self.runner.invoke(build, ['--project=admin/foo',
                                   '--build=1',
                                   'stop',
                                   '-y'])
        assert stop.call_count == 1

    @patch('polyaxon_client.api.build_job.BuildJobApi.get_statuses')
    def test_build_statuses(self, get_statuses):
        self.runner.invoke(build, ['--project=admin/foo', '--build=1', 'statuses'])
        assert get_statuses.call_count == 1

    @patch('polyaxon_client.api.build_job.BuildJobApi.bookmark')
    def test_build_bookmark(self, bookmark):
        self.runner.invoke(build, ['--project=admin/foo', '--build=1', 'bookmark'])
        assert bookmark.call_count == 1

    @patch('polyaxon_client.api.build_job.BuildJobApi.unbookmark')
    def test_build_unbookmark(self, unbookmark):
        self.runner.invoke(build, ['--project=admin/foo', '--build=1', 'unbookmark'])
        assert unbookmark.call_count == 1
