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
from repos.models import Repo, RepoRevision
from repos.serializers import RepoSerializer

from tests.factories.factory_clusters import ClusterFactory
from tests.factories.factory_repos import RepoFactory
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

        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/projects/{}/repo/upload'.format(API_V1, self.object.project.uuid.hex)
        settings.MEDIA_ROOT = tempfile.mkdtemp()

    def test_video_uploaded(self):
        user = self.auth_client.user
        repo_name = self.object.project.name
        filename = 'repo'
        file = File(open('./tests/static/repo.tar.gz', 'rb'))
        uploaded_file = SimpleUploadedFile(filename, file.read(),
                                           content_type='multipart/form-data')
        with patch('repos.tasks.handle_new_files.delay') as mock_task:
            self.auth_client.put(self.url,
                                 data={'file': uploaded_file},
                                 content_type=MULTIPART_CONTENT)
        file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT, user.username, repo_name)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
