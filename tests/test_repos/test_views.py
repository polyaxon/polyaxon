import json
import os

from unittest.mock import patch

import pytest

from rest_framework import status

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.test.client import MULTIPART_CONTENT

import conf

from api.repos.serializers import ExternalRepoSerializer, RepoSerializer
from api.utils.views.protected import ProtectedView
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.repos import ExternalRepo, Repo
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import ExternalRepoFactory, RepoFactory
from factories.factory_users import UserFactory
from libs.repos import git
from tests.utils import BaseViewTest


@pytest.mark.repos_mark
class TestRepoDetailViewV1(BaseViewTest):
    serializer_class = RepoSerializer
    model_class = Repo
    factory_class = RepoFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=self.project)
        self.unauthorised_object = self.factory_class()
        self.url = '/{}/{}/{}/repo'.format(API_V1,
                                           self.project.user.username,
                                           self.project.name)
        self.unauthorised_url = '/{}/{}/{}/repo'.format(
            API_V1,
            self.unauthorised_object.project.user.username,
            self.unauthorised_object.project.name)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

        # unauthorised object get works
        resp = self.auth_client.get(self.unauthorised_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.unauthorised_object).data

    def test_delete(self):
        assert self.model_class.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 1

        # unauthorised object delete not working
        resp = self.auth_client.delete(self.unauthorised_url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.repos_mark
class TestExternalRepoDetailViewV1(BaseViewTest):
    serializer_class = ExternalRepoSerializer
    model_class = ExternalRepo
    factory_class = ExternalRepoFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.object = ExternalRepo.objects.create(project=self.project,
                                                  git_url='https://github.com/polyaxon/empty.git')
        self.unauthorised_object = self.factory_class(
            git_url='https://github.com/polyaxon/empty.git')
        self.url = '/{}/{}/{}/repo'.format(API_V1,
                                           self.project.user.username,
                                           self.project.name)
        self.unauthorised_url = '/{}/{}/{}/repo'.format(
            API_V1,
            self.unauthorised_object.project.user.username,
            self.unauthorised_object.project.name)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

        # unauthorised object get works
        resp = self.auth_client.get(self.unauthorised_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.unauthorised_object).data

    def test_delete(self):
        assert self.model_class.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 1

        # unauthorised object delete not working
        resp = self.auth_client.delete(self.unauthorised_url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.repos_mark
class TestRepoUploadView(BaseViewTest):
    model_class = Repo
    factory_class = RepoFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/repo/upload'.format(API_V1,
                                                  self.project.user.username,
                                                  self.project.name)

    @staticmethod
    def get_upload_file(filename='repo'):
        file = File(open('./tests/fixtures_static/{}.tar.gz'.format(filename), 'rb'))
        return SimpleUploadedFile(filename, file.read(),
                                  content_type='multipart/form-data')

    def test_upload_files_synchronously_creates_repo(self):
        user = self.auth_client.user
        repo_name = self.project.name

        # No repo was created yet
        assert self.model_class.objects.count() == 0
        repo_path = '{}/{}/{}/{}'.format(conf.get('REPOS_MOUNT_PATH'),
                                         user.username,
                                         repo_name,
                                         repo_name)
        self.assertFalse(os.path.exists(repo_path))

        uploaded_file = self.get_upload_file()

        with patch('api.repos.views.handle_new_files') as mock_task:
            self.auth_client.put(self.url,
                                 data={'repo': uploaded_file, 'json': json.dumps({'delay': False})},
                                 content_type=MULTIPART_CONTENT)

        file_path = '{}/{}/{}.tar.gz'.format(conf.get('UPLOAD_MOUNT_PATH'),
                                             user.username,
                                             repo_name)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
        assert self.model_class.objects.count() == 1
        self.assertTrue(os.path.exists(repo_path))

    def test_upload_files_creates_repo(self):
        user = self.auth_client.user
        repo_name = self.project.name

        # No repo was created yet
        assert self.model_class.objects.count() == 0
        repo_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, repo_name, repo_name)
        self.assertFalse(os.path.exists(repo_path))

        uploaded_file = self.get_upload_file()

        with patch('api.repos.views.handle_new_files') as mock_task:
            self.auth_client.put(self.url,
                                 data={'repo': uploaded_file},
                                 content_type=MULTIPART_CONTENT)
        file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
        assert self.model_class.objects.count() == 1
        self.assertTrue(os.path.exists(repo_path))

    def test_upload_files_uses_repo_if_exists(self):
        user = self.auth_client.user
        repo_name = self.project.name

        repo_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, repo_name, repo_name)
        self.assertFalse(os.path.exists(repo_path))

        repo = self.factory_class(project=self.project)
        assert self.model_class.objects.count() == 1
        self.assertTrue(os.path.exists(repo_path))

        uploaded_file = self.get_upload_file()

        with patch('api.repos.views.handle_new_files') as mock_task:
            self.auth_client.put(self.url,
                                 data={'repo': uploaded_file},
                                 content_type=MULTIPART_CONTENT)
        file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
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
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        upload_file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
        # Assert the the task handler takes care of cleaning the upload root after
        # committing changes
        self.assertFalse(os.path.exists(upload_file_path))

        # Assert repo model was created
        assert self.model_class.objects.count() == 1
        repo = self.model_class.objects.first()

        # Assert new git repo was created in the repos root and that also the tar file was deleted
        code_file_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, self.project.name, self.project.name)
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
        new_uploaded_file = self.get_upload_file('updated_repo')
        self.auth_client.put(self.url,
                             data={'repo': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        upload_file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
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
        assert commit.author.email == user.email
        assert commit.author.name == user.username
        # Assert that we committed 3 files (2 files in new_repo.tar.gz one file was deleted)
        assert len(git.get_committed_files(code_file_path, commit_hash)) == 3

        # Make a new upload with repo_with_folder.tar.gz containing 1 file one dir with fil
        new_uploaded_file = self.get_upload_file('repo_with_folder')
        self.auth_client.put(self.url,
                             data={'repo': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        upload_file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
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
        assert commit.author.email == user.email
        assert commit.author.name == user.username
        # Assert that we committed 3 files
        # (1 file updated 1 deleted, and one folder with 1 file added)
        assert len(git.get_committed_files(code_file_path, commit_hash)) == 3

        # Check that other user cannot commit to this repo
        new_user = UserFactory()
        self.auth_client.login_user(new_user)
        new_uploaded_file = self.get_upload_file('updated_repo')
        response = self.auth_client.put(self.url,
                                        data={'repo': new_uploaded_file},
                                        content_type=MULTIPART_CONTENT)

        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        upload_file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), new_user.username, repo_name)
        # Assert the the task handler takes care of cleaning the upload root after
        # committing changes
        self.assertFalse(os.path.exists(upload_file_path))

        # Assert same git repo was used in the repos root and that also the tar file was deleted
        self.assertFalse(os.path.exists(tar_code_file_path))
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        self.assertTrue(os.path.exists(git_file_path))
        # Get last commit and check it did not change
        new_commit_hash, new_commit = git.get_last_commit(code_file_path)
        assert commit.author.email == new_commit.author.email
        assert commit.author.name == new_commit.author.name
        assert new_commit_hash == commit_hash

        # Log old user, otherwise other tests will crash
        self.auth_client.login_user(user)

    def test_cannot_upload_if_project_has_a_running_notebook_serverless(self):
        user = self.auth_client.user
        repo_name = self.project.name

        # Update project with has_notebook True
        notebook = NotebookJobFactory(project=self.project)
        notebook.set_status(status=JobLifeCycle.RUNNING)

        assert self.model_class.objects.count() == 0

        uploaded_file = self.get_upload_file()

        with patch('api.repos.views.handle_new_files') as mock_task:
            response = self.auth_client.put(self.url,
                                            data={'repo': uploaded_file},
                                            content_type=MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_200_OK
        file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
        # No new repo was not created and still exists
        assert self.model_class.objects.count() == 1
        repo_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, repo_name, repo_name)
        self.assertTrue(os.path.exists(repo_path))

    @override_settings(MOUNT_CODE_IN_NOTEBOOKS=True)
    def test_cannot_upload_if_project_has_a_running_notebook_with_code_mount(self):
        user = self.auth_client.user
        repo_name = self.project.name

        # Update project with has_notebook True
        notebook = NotebookJobFactory(project=self.project)
        notebook.set_status(status=JobLifeCycle.RUNNING)

        assert self.model_class.objects.count() == 0

        uploaded_file = self.get_upload_file()

        with patch('api.repos.views.handle_new_files') as mock_task:
            response = self.auth_client.put(self.url,
                                            data={'repo': uploaded_file},
                                            content_type=MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
        self.assertFalse(os.path.exists(file_path))
        assert mock_task.call_count == 0
        # No new repo was not created and still exists
        assert self.model_class.objects.count() == 0
        repo_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, repo_name, repo_name)
        self.assertFalse(os.path.exists(repo_path))

    def test_cannot_upload_if_project_has_external_repo(self):
        user = self.auth_client.user
        repo_name = self.project.name
        repo = ExternalRepo(project=self.project, git_url='https://github.com/polyaxon/empty.git')
        repo.save()

        assert self.model_class.objects.count() == 0

        uploaded_file = self.get_upload_file()

        with patch('api.repos.views.handle_new_files') as mock_task:
            response = self.auth_client.put(self.url,
                                            data={'repo': uploaded_file},
                                            content_type=MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        file_path = '{}/{}/{}.tar.gz'.format(
            conf.get('UPLOAD_MOUNT_PATH'), user.username, repo_name)
        self.assertFalse(os.path.exists(file_path))
        assert mock_task.call_count == 0
        # No new repo was not created and still exists
        assert self.model_class.objects.count() == 0
        repo_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, repo_name, repo_name)
        self.assertFalse(os.path.exists(repo_path))


@pytest.mark.repos_mark
class RepoDownloadViewTest(BaseViewTest):
    model_class = Repo
    factory_class = RepoFactory
    HAS_AUTH = True
    HAS_INTERNAL = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.upload_url = '/{}/{}/{}/repo/upload'.format(API_V1,
                                                         self.project.user.username,
                                                         self.project.name)
        self.download_url = '/{}/{}/{}/repo/download'.format(API_V1,
                                                             self.project.user.username,
                                                             self.project.name)
        self.url = self.download_url

    def upload_file(self):
        filename = 'repo'
        file = File(open('./tests/fixtures_static/{}.tar.gz'.format(filename), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, file.read(),
                                           content_type='multipart/form-data')
        self.auth_client.put(self.upload_url,
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

    def test_raise_404_if_repo_does_not_exist(self):
        response = self.auth_client.get(self.download_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_redirects_nginx_to_file_for_internal_repos(self):
        self.upload_file()
        user = self.auth_client.user
        code_file_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, self.project.name, self.project.name)
        # Assert that the code_file_path exists
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        git_file_path = '{}/.git'.format(code_file_path)
        self.assertTrue(os.path.exists(git_file_path))

        response = self.auth_client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        self.assertEqual(
            response[ProtectedView.NGINX_REDIRECT_HEADER],
            '{}/{}-master.tar.gz'.format(conf.get('REPOS_ARCHIVE_ROOT'), self.project.name))

    def test_redirects_nginx_to_file_for_external_repos(self):
        ExternalRepo.objects.create(project=self.project,
                                    git_url='https://github.com/polyaxon/empty.git')
        user = self.auth_client.user
        code_file_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, self.project.name, 'empty')
        # Assert that the code_file_path exists
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        git_file_path = '{}/.git'.format(code_file_path)
        self.assertTrue(os.path.exists(git_file_path))

        response = self.auth_client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        self.assertEqual(
            response[ProtectedView.NGINX_REDIRECT_HEADER],
            '{}/{}-master.tar.gz'.format(conf.get('REPOS_ARCHIVE_ROOT'), self.project.name))

    def test_redirects_nginx_to_file_works_with_internal_client(self):
        self.upload_file()
        user = self.auth_client.user
        code_file_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, self.project.name, self.project.name)
        # Assert that the code_file_path exists
        self.assertTrue(os.path.exists(code_file_path))
        # Assert that the code_file_path is a git repo
        git_file_path = '{}/.git'.format(code_file_path)
        self.assertTrue(os.path.exists(git_file_path))

        response = self.internal_client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        self.assertEqual(
            response[ProtectedView.NGINX_REDIRECT_HEADER],
            '{}/{}-master.tar.gz'.format(conf.get('REPOS_ARCHIVE_ROOT'), self.project.name))


@pytest.mark.repos_mark
class TestExternalRepoSetView(BaseViewTest):
    model_class = ExternalRepo
    factory_class = ExternalRepoFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/repo/external'.format(API_V1,
                                                    self.project.user.username,
                                                    self.project.name)

    def test_set_external_repo(self):
        user = self.auth_client.user
        repo_name = 'empty'

        # No repo was created yet
        assert self.model_class.objects.count() == 0
        repo_path = '{}/{}/{}/{}'.format(
            conf.get('REPOS_MOUNT_PATH'), user.username, self.project.name, repo_name)
        self.assertFalse(os.path.exists(repo_path))

        response = self.auth_client.post(self.url,
                                         data={'git_url': 'https://github.com/polyaxon/empty.git'})
        assert response.status_code == status.HTTP_201_CREATED
        self.assertTrue(os.path.exists(repo_path))

        # Trying to reset same repo
        response = self.auth_client.post(self.url,
                                         data={'git_url': 'https://github.com/polyaxon/empty.git'})
        assert response.status_code == status.HTTP_200_OK
        self.assertTrue(os.path.exists(repo_path))

        # Trying to reset different repo
        response = self.auth_client.post(self.url,
                                         data={'git_url': 'https://github.com/polyaxon/foo.git'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self.assertTrue(os.path.exists(repo_path))

    def test_set_wrong_external_repo(self):
        response = self.auth_client.post(self.url,
                                         data={'git_url': 'https://github.com/foo/bar.git',
                                               'is_public': False})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.repos_mark
class TestExternalRepoSyncView(BaseViewTest):
    model_class = ExternalRepo
    factory_class = ExternalRepoFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/repo/sync'.format(API_V1,
                                                self.project.user.username,
                                                self.project.name)
        self.set_url = '/{}/{}/{}/repo/external'.format(API_V1,
                                                        self.project.user.username,
                                                        self.project.name)
        self.enable_url = '/{}/{}/{}/ci'.format(API_V1,
                                                self.project.user.username,
                                                self.project.name)

    def test_sync_non_existing_repo(self):
        # Trying to sync a non existing repo
        response = self.auth_client.post(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_sync_works(self):
        assert self.model_class.objects.count() == 0
        response = self.auth_client.post(self.set_url,
                                         data={'git_url': 'https://github.com/polyaxon/empty.git'})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == 1
        repo = self.model_class.objects.last()
        commit = git.get_last_commit(repo_path=repo.path)

        # Enable CI
        response = self.auth_client.post(self.enable_url)
        assert response.status_code == status.HTTP_201_CREATED

        # Adding a new commit
        open('{}/foo'.format(repo.path), 'w')
        git.commit(repo.path, 'user@domain.com', 'username')
        assert git.get_last_commit(repo_path=repo.path) != commit

        # Sync must remove that commit
        response = self.auth_client.post(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert git.get_last_commit(repo_path=repo.path) == commit
