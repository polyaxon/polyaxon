import os

import pytest

import conf

from db.models.repos import ExternalRepo
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from libs.repos import git
from libs.repos.git import GitCloneException
from tests.utils import BaseTest


@pytest.mark.repos_mark
class TestRepoModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()

    def test_repo_creation_results_in_repo_path_creation_deletion_results_in_path_deletion(self):
        repo_path = '{}/{}/{}/{}'.format(conf.get('REPOS_MOUNT_PATH'),
                                         self.project.user.username,
                                         self.project.name,
                                         self.project.name)
        self.assertFalse(os.path.exists(repo_path))

        # Create repo
        repo = RepoFactory(project=self.project)
        assert repo.path == repo_path

        self.assertTrue(os.path.exists(repo_path))
        git_file_path = '{}/.git'.format(repo_path)
        self.assertTrue(os.path.exists(git_file_path))

        # Delete repo
        repo.delete()
        self.assertFalse(os.path.exists(repo_path))

    def test_checkout_commit_and_master(self):
        git_url = 'https://github.com/polyaxon/empty.git'

        # Create repo
        repo = ExternalRepo(project=self.project, git_url=git_url)
        repo.save()

        # Check last commit
        assert len(repo.last_commit) == 2

        # Add new file
        file_path = os.path.join(repo.path, 'file1.dat')
        open(file_path, 'w+')

        assert git.get_status(repo.path) is not None
        git.commit(repo.path, 'user@domain.com', 'username')

        # Check last commit
        commit1 = repo.last_commit[0]
        assert commit1 is not None

        # Add new file
        file_path = os.path.join(repo.path, 'file2.dat')
        open(file_path, 'w+')

        assert git.get_status(repo.path) is not None
        git.commit(repo.path, 'user@domain.com', 'username')

        # Check last commit
        commit2 = repo.last_commit[0]
        assert commit2 is not None

        # Commits are different
        assert commit1 != commit2

        # Checkout to commit1
        git.checkout_commit(repo_path=repo.path, commit=commit1)
        assert repo.last_commit[0] == commit1

        # Checkout to master
        git.checkout_commit(repo_path=repo.path)
        assert repo.last_commit[0] == commit2

    def test_private_external_repo_with_wrong_auth(self):
        git_url = 'https://git.com/foo/bar.git'
        # Create repo
        with self.assertRaises(GitCloneException):
            repo = ExternalRepo(project=self.project, git_url=git_url, is_public=False)
            repo.save()

    def test_private_external_repo_with_no_repos_access_token(self):
        git_url = 'https://github.com/foo/bar.git'

        # Create repo
        with self.assertRaises(GitCloneException):
            repo = ExternalRepo(project=self.project, git_url=git_url, is_public=False)
            repo.save()
