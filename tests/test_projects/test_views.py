# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status

from api.urls import API_V1
from experiments.models import Experiment
from experiments.serializers import ExperimentSerializer
from projects.models import (
    Project,
    Polyaxonfile,
)
from projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    PolyaxonfileSerializer,
)
from tests.factories.factory_experiments import ExperimentFactory
from tests.factories.factory_projects import (
    ProjectFactory,
    PolyaxonfileFactory,
)
from tests.utils import BaseTest


class TestProjectListViewV1(BaseTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.url = '/{}/projects/'.format(API_V1)
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
        data = {'name': 'new_project'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1


class TestProjectDetailViewV1(BaseTest):
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.object = self.factory_class()
        self.url = '/{}/projects/{}/'.format(API_V1, self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            PolyaxonfileFactory(project=self.object)

        for i in range(1):
            ExperimentFactory(project=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['experiments']) == 1
        assert resp.data['experiments'] == ExperimentSerializer(self.object.experiments.all(),
                                                                many=True).data
        assert len(resp.data['polyaxonfiles']) == 2
        assert resp.data['polyaxonfiles'] == PolyaxonfileSerializer(self.object.polyaxonfiles.all(),
                                                                    many=True).data

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
        assert new_object.experiments.count() == 1
        assert new_object.polyaxonfiles.count() == 2

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert Polyaxonfile.objects.count() == 2
        assert Experiment.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0
        assert Polyaxonfile.objects.count() == 0
        assert Experiment.objects.count() == 0


class TestProjectPolyaxonfileListViewV1(BaseTest):
    serializer_class = PolyaxonfileSerializer
    model_class = Polyaxonfile
    factory_class = PolyaxonfileFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.url = '/{}/projects/{}/polyaxonfiles/'.format(API_V1, self.project.uuid.hex)
        self.objects = [self.factory_class(project=self.project)
                        for _ in range(self.num_objects)]
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

        data = {'content': """----
        version: v1
        model:
          model_type: classifie"""}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.content == data['content']
