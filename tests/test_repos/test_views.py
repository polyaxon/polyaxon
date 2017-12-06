# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile
import uuid

from unittest.mock import patch

import os
from rest_framework import status

from django.test.client import MULTIPART_CONTENT

from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from api.urls import API_V1
from repos import git
from repos.models import Repo, RepoRevision
from repos.serializers import RepoSerializer

from tests.factories.factory_clusters import ClusterFactory
from tests.factories.factory_projects import ProjectFactory
from tests.factories.factory_repos import RepoFactory
from tests.factories.factory_users import UserFactory
from tests.utils import BaseViewTest


class TestRepoDetailViewV1(BaseViewTest):
    serializer_class = RepoSerializer
    model_class = Repo
    factory_class = RepoFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        cluster = ClusterFactory()
        self.object = self.factory_class(user=cluster.user)
        self.url = '/{}/projects/{}/repo'.format(API_V1, self.object.project.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            RepoRevision(repo=self.object, user=cluster.user, commit=uuid.uuid4().hex).save()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert RepoRevision.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0
        assert RepoRevision.objects.count() == 0


class TestUploadFilesView(BaseViewTest):
    model_class = Repo
    factory_class = RepoFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/projects/{}/repo/upload'.format(API_V1, self.project.uuid.hex)
        settings.REPOS_ROOT = tempfile.mkdtemp()
        settings.UPLOAD_ROOT = tempfile.mkdtemp()

    def get_upload_file(self, filename='repo'):
        file = File(open('./tests/fixtures_static/{}.tar.gz'.format(filename), 'rb'))
        return SimpleUploadedFile(filename, file.read(),
                                  content_type='multipart/form-data')

    def test_upload_files_creates_repo(self):
        user = self.auth_client.user
        repo_name = self.project.name

        # No repo was created yet
        assert self.model_class.objects.count() == 0
        repo_path = '{}/{}/{}'.format(settings.REPOS_ROOT, user.username, repo_name)
        self.assertFalse(os.path.exists(repo_path))

        uploaded_file = self.get_upload_file()

        with patch('repos.tasks.handle_new_files.delay') as mock_task:
            self.auth_client.put(self.url,
                                 data={'file': uploaded_file},
                                 content_type=MULTIPART_CONTENT)
        file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT, user.username, repo_name)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
        assert self.model_class.objects.count() == 1
        self.assertTrue(os.path.exists(repo_path))

    def test_upload_files_uses_repo_if_exists(self):
        user = self.auth_client.user
        repo_name = self.project.name

        repo_path = '{}/{}/{}'.format(settings.REPOS_ROOT, user.username, repo_name)
        self.assertFalse(os.path.exists(repo_path))

        repo = self.factory_class(project=self.project, user=user)
        assert self.model_class.objects.count() == 1
        self.assertTrue(os.path.exists(repo_path))

        uploaded_file = self.get_upload_file()

        with patch('repos.tasks.handle_new_files.delay') as mock_task:
            self.auth_client.put(self.url,
                                 data={'file': uploaded_file},
                                 content_type=MULTIPART_CONTENT)
        file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT, user.username, repo_name)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
        # No new repo was created and still exists
        assert self.model_class.objects.count() == 1
        self.assertTrue(os.path.exists(repo_path))

        # Deleting repo deletes the dir
        repo.delete()
        self.assertFalse(os.path.exists(repo_path))

    def test_handle_new_files_task(self):
        assert self.model_class.objects.count() == 0
        user = self.auth_client.user
        repo_name = self.project.name
        uploaded_file = self.get_upload_file()

        self.auth_client.put(self.url,
                             data={'file': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        upload_file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT, user.username, repo_name)
        # Assert the the task handler takes care of cleaning the upload root after
        # committing changes
        self.assertFalse(os.path.exists(upload_file_path))

        # Assert repo model was created
        assert self.model_class.objects.count() == 1
        repo = self.model_class.objects.first()

        # Assert new git repo was created in the repos root and that also the tar file was deleted
        code_file_path = '{}/{}/{}'.format(settings.REPOS_ROOT, user.username, self.project.name)
        tar_code_file_path = repo.get_tmp_tar_path()
        self.assertFalse(os.path.exists(tar_code_file_path))
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        git_file_path = '{}/.git'.format(code_file_path)
        self.assertTrue(os.path.exists(git_file_path))
        # Get last commit
        commit_hash, commit = git.get_last_commit(code_file_path)
        assert commit.author.email == user.email
        assert commit.author.name == user.username

        # Make a new upload with repo_new.tar.gz containing 2 files
        new_user = UserFactory()
        self.auth_client.login_user(new_user)
        new_uploaded_file = self.get_upload_file('updated_repo')
        self.auth_client.put(self.url,
                             data={'file': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        upload_file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT,
                                                    new_user.username,
                                                    repo_name)
        # Assert the the task handler takes care of cleaning the upload root after
        # committing changes
        self.assertFalse(os.path.exists(upload_file_path))

        # Assert same git repo was used in the repos root and that also the tar file was deleted
        self.assertFalse(os.path.exists(tar_code_file_path))
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        self.assertTrue(os.path.exists(git_file_path))
        # Get last commit
        commit_hash, commit = git.get_last_commit(code_file_path)
        assert commit.author.email == new_user.email
        assert commit.author.name == new_user.username
        # Assert that we committed 3 files (2 files in new_repo.tar.gz one file was deleted)
        assert len(git.get_committed_files(code_file_path, commit_hash)) == 3
        assert repo.revisions.count() == 2

        # Make a new upload with repo_with_folder.tar.gz containing 1 file one dir with file
        new_user = UserFactory()
        self.auth_client.login_user(new_user)
        new_uploaded_file = self.get_upload_file('repo_with_folder')
        self.auth_client.put(self.url,
                             data={'file': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        upload_file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT,
                                                    new_user.username,
                                                    repo_name)
        # Assert the the task handler takes care of cleaning the upload root after
        # committing changes
        self.assertFalse(os.path.exists(upload_file_path))

        # Assert same git repo was used in the repos root and that also the tar file was deleted
        self.assertFalse(os.path.exists(tar_code_file_path))
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        self.assertTrue(os.path.exists(git_file_path))
        # Get last commit
        commit_hash, commit = git.get_last_commit(code_file_path)
        assert commit.author.email == new_user.email
        assert commit.author.name == new_user.username
        # Assert that we committed 3 files
        # (1 file updated 1 deleted, and one folder with 1 file added)
        import pdb; pdb.set_trace()
        assert len(git.get_committed_files(code_file_path, commit_hash)) == 3
        assert repo.revisions.count() == 3

        # login old user
        self.auth_client.login_user(user)
