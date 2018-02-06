# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings
from django.db import IntegrityError

from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from repos import git
from repos.models import ExternalRepo
from tests.utils import BaseTest


class TestRepoModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()

    def test_repo_creation_results_in_repo_path_creation_deletion_results_in_path_deletion(self):
        repo_path = '{}/{}/{}/{}'.format(settings.REPOS_ROOT,
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

    def test_external_repo_creation_and_deletion(self):
        repo_path = '{}/{}/{}/{}'.format(settings.REPOS_ROOT,
                                         self.project.user.username,
                                         self.project.name,
                                         'empty')
        self.assertFalse(os.path.exists(repo_path))

        git_url = 'https://github.com/polyaxon/empty.git'

        # Create repo
        repo = ExternalRepo(project=self.project, git_url=git_url)
        repo.save()
        assert repo.path == repo_path
        assert repo.name == 'empty'

        self.assertTrue(os.path.exists(repo_path))
        git_file_path = '{}/.git'.format(repo_path)
        self.assertTrue(os.path.exists(git_file_path))

        # Test fetch works correctly
        git.fetch(repo.git_url, repo.path)

        # Test query model works
        assert repo == ExternalRepo.objects.get(project=self.project, git_url=git_url)

        # Check last commit
        assert repo.last_commit is None

        # Delete repo
        repo.delete()
        self.assertFalse(os.path.exists(repo_path))

    def test_checkout_commit_and_master(self):
        git_url = 'https://github.com/polyaxon/empty.git'

        # Create repo
        repo = ExternalRepo(project=self.project, git_url=git_url)
        repo.save()

        # Check last commit
        assert repo.last_commit is None

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
