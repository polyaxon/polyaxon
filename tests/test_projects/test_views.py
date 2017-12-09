# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status

from api.urls import API_V1
from experiments.models import Experiment
from experiments.serializers import ExperimentSerializer
from projects.models import (
    Project,
    ExperimentGroup,
)
from projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    ExperimentGroupSerializer,
)
from factories.factory_clusters import ClusterFactory
from factories.factory_projects import (
    ProjectFactory,
    ExperimentGroupFactory,
)
from tests.utils import BaseViewTest


class TestProjectListViewV1(BaseViewTest):
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


class TestProjectDetailViewV1(BaseViewTest):
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        cluster = ClusterFactory()
        self.object = self.factory_class(user=cluster.user)
        self.url = '/{}/projects/{}/'.format(API_V1, self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            ExperimentGroupFactory(project=self.object, user=cluster.user)

        # creating the default factory should trigger the creation of one experiment per group
        assert Experiment.objects.count() == 2

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['experiments']) == 2
        assert resp.data['experiments'] == ExperimentSerializer(self.object.experiments.all(),
                                                                many=True).data
        assert len(resp.data['experiment_groups']) == 2
        assert resp.data['experiment_groups'] == ExperimentGroupSerializer(
            self.object.experiment_groups.all(), many=True).data

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
        assert new_object.experiments.count() == 2
        assert new_object.experiment_groups.count() == 2

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert Experiment.objects.count() == 0


class TestProjectExperimentGroupListViewV1(BaseViewTest):
    serializer_class = ExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        cluster = ClusterFactory(user=self.auth_client.user)
        self.project = ProjectFactory(user=cluster.user)
        self.url = '/{}/projects/{}/experiment_groups/'.format(API_V1, self.project.uuid.hex)
        self.objects = [self.factory_class(project=self.project, user=cluster.user)
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
        content = """---
version: 1
project:
  name: project1

model:
  model_type: classifier

  graph:
    input_layers: images
    layers:
      - Conv2D:
          filters: 64
          kernel_size: [3, 3]
          strides: [1, 1]
          activation: relu
          kernel_initializer: Ones"""

        data = {'content': content}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.content == data['content']
