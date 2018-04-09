import os

from django.conf import settings

from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from libs.paths import copy_to_tmp_dir, get_tmp_path
from tests.utils import BaseTest


class TestPaths(BaseTest):
    def test_copy_repo_path_to_tmp_dir(self):
        project = ProjectFactory()
        repo_path = '{}/{}/{}/{}'.format(settings.REPOS_ROOT,
                                         project.user.username,
                                         project.name,
                                         project.name)
        self.assertFalse(os.path.exists(repo_path))

        repo = RepoFactory(project=project)
        assert repo.path == repo_path
        self.assertTrue(os.path.exists(repo_path))
        git_file_path = '{}/.git'.format(repo_path)
        self.assertTrue(os.path.exists(git_file_path))

        copy_to_tmp_dir(repo_path, 'new')
        git_file_path = '{}/.git'.format(get_tmp_path('new'))
        self.assertTrue(os.path.exists(git_file_path))
