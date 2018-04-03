from unittest.mock import patch

from rest_framework import status

from factories.factory_experiments import ExperimentStatusFactory, ExperimentFactory
from factories.factory_projects import ProjectFactory
from polyaxon.urls import API_V1
from experiment_groups.models import (
    ExperimentGroup,
)
from experiment_groups.serializers import (
    ExperimentGroupSerializer,
)
from factories.factory_experiment_groups import (
    ExperimentGroupFactory,
)
from spawners.utils.constants import ExperimentLifeCycle
from tests.utils import BaseViewTest


class TestProjectExperimentGroupListViewV1(BaseViewTest):
    serializer_class = ExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/groups/'.format(API_V1,
                                              self.project.user.username,
                                              self.project.name)
        self.other_url = '/{}/{}/{}/groups/'.format(API_V1,
                                                    self.other_project.user.username,
                                                    self.other_project.name)

        with patch('dockerizer.builders.experiments.build_experiment') as _:
            with patch('schedulers.experiment_scheduler.start_experiment') as _:
                self.objects = [self.factory_class(project=self.project)
                                for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter(project=self.project)
        # Other objects
        self.other_object = self.factory_class(project=self.other_project)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data['results']
        assert data[0] == self.serializer_class(self.other_object).data

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

    def test_create_raises_with_content_for_independent_experiment(self):
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

        data = {'content': content, 'description': 'new-deep'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.queryset.count() == self.num_objects

    def test_create_with_valid_group(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        content = """---
version: 1
project:
  name: project1

settings:
    concurrent_experiments: 3

matrix:
  lr:
    values: [0.1, 0.2, 0.3]

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

        data = {'content': content, 'description': 'new-deep'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.content == data['content']


class TestStopExperimentGroupViewV1(BaseViewTest):
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as _:
            self.object = self.factory_class(project=project)
        # Add a running experiment
        experiment = ExperimentFactory(experiment_group=self.object)
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        self.url = '/{}/{}/{}/groups/{}/stop'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.sequence)

    def test_stop_all(self):
        data = {}
        assert self.object.stopped_experiments.count() == 0

        # Check that is calling the correct function
        with patch('experiment_groups.tasks.stop_group_experiments.delay') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1

        # Execute the function
        with patch('schedulers.experiment_scheduler.stop_experiment') as _:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_200_OK
        assert self.object.stopped_experiments.count() == 2

    def test_stop_pending(self):
        data = {'pending': True}
        assert self.object.stopped_experiments.count() == 0

        # Check that is calling the correct function
        with patch('experiment_groups.tasks.stop_group_experiments.delay') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1

        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.stopped_experiments.count() == 2
