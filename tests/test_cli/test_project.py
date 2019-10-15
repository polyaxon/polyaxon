# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.project import project


class TestProject(BaseCommandTestCase):
    @patch('polyaxon.client.api.project.ProjectApi.create_project')
    def test_create_project(self, create_project):
        self.runner.invoke(project, 'create')
        assert create_project.call_count == 0
        self.runner.invoke(project, ['create', '--name=foo'])
        assert create_project.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.list_projects')
    def test_list_projects(self, list_projects):
        self.runner.invoke(project, ['list'])
        assert list_projects.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.get_project')
    def test_get_project(self, get_project):
        self.runner.invoke(project, ['-p admin/foo', 'get'])
        assert get_project.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.update_project')
    def test_update_project(self, update_project):
        self.runner.invoke(project, ['update'])
        assert update_project.call_count == 0

        self.runner.invoke(project, ['-p admin/foo', 'update', '--description=foo'])
        assert update_project.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.list_experiments')
    def test_project_experiment(self, list_experiments):
        self.runner.invoke(project, ['-p admin/foo', 'experiments'])
        assert list_experiments.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.list_tensorboards')
    def test_project_tensorboards(self, list_tensorboards):
        self.runner.invoke(project, ['-p admin/foo', 'tensorboards'])
        assert list_tensorboards.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.download_repo')
    def test_project_download_repo(self, download_repo):
        self.runner.invoke(project, ['-p admin/foo', 'download'])
        assert download_repo.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.bookmark')
    def test_project_bookmark(self, bookmark):
        self.runner.invoke(project, ['-p admin/foo', 'bookmark'])
        assert bookmark.call_count == 1

    @patch('polyaxon.client.api.project.ProjectApi.unbookmark')
    def test_project_unbookmark(self, unbookmark):
        self.runner.invoke(project, ['-p admin/foo', 'unbookmark'])
        assert unbookmark.call_count == 1
