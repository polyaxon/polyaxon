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


class TestRepoListViewV1(BaseViewTest):
    serializer_class = RepoSerializer
    model_class = Repo
    factory_class = RepoFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.url = '/{}/repos/'.format(API_V1)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next = resp.data.get('next')
        assert next is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        data = {'name': 'new_repo'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1


class TestRepoDetailViewV1(BaseViewTest):
    serializer_class = RepoSerializer
    model_class = Repo
    factory_class = RepoFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        cluster = ClusterFactory()
        self.object = self.factory_class(user=cluster.user)
        self.url = '/{}/repos/{}/'.format(API_V1, self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            RepoRevision(repo=self.object, user=cluster.user, commit=uuid.uuid4().hex).save()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        new_name = 'updated_project_name'
        data = {'name': new_name}
        assert self.object.name != data['name']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.name != self.object.name
        assert new_object.name == new_name
        assert new_object.revisions.count() == 2

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
        self.url = '/{}/repos/{}/upload'.format(API_V1, self.object.uuid.hex)
        settings.MEDIA_ROOT = tempfile.mkdtemp()

    def test_video_uploaded(self):
        user = self.auth_client.user
        repo = self.object.name
        filename = 'repo'
        file = File(open('./tests/static/repo.tar.gz', 'rb'))
        uploaded_file = SimpleUploadedFile(filename, file.read(),
                                           content_type='multipart/form-data')
        with patch('repos.tasks.handle_new_files.delay') as mock_task:
            self.auth_client.put(self.url,
                                 data={'file': uploaded_file},
                                 content_type=MULTIPART_CONTENT)
        file_path = '{}/{}/{}.tar.gz'.format(settings.UPLOAD_ROOT, user.username, repo)
        self.assertTrue(os.path.exists(file_path))
        assert mock_task.call_count == 1
