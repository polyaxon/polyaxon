from unittest.mock import patch

import pytest
from rest_framework import status

from api.experiment_groups.serializers import (
    ExperimentGroupDetailSerializer,
    ExperimentGroupSerializer
)
from constants.experiments import ExperimentLifeCycle
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory, ExperimentStatusFactory
from factories.factory_projects import ProjectFactory
from polyaxon.urls import API_V1
from tests.utils import BaseViewTest


@pytest.mark.experiment_groups_mark
class TestProjectExperimentGroupListViewV1(BaseViewTest):
    serializer_class = ExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_RUNNER = True

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
        self.other_object.refresh_from_db()
        assert data[0] == self.serializer_class(self.other_object).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_create_raises_with_content_for_independent_experiment(self):
        data = {'check_specification': True}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        content = """---
version: 1

kind: group

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
        data = {'check_specification': True}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        content = """---
version: 1

kind: group

settings:
    concurrency: 3
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
        assert last_object.params is not None
        assert last_object.params['concurrency'] == 3
        assert last_object.params['matrix']['lr'] is not None

    def test_create_without_content_passes_if_no_spec_validation_requested(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.content is None

    def test_create_with_params(self):
        data = {
            'params': {
                'concurrency': 3,
                'matrix': {
                    'lr': {'values': [0.1, 0.2, 0.3]}
                }
            }
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.content is None


@pytest.mark.experiment_groups_mark
class TestExperimentGroupDetailViewV1(BaseViewTest):
    serializer_class = ExperimentGroupDetailSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/groups/{}/'.format(API_V1,
                                                 project.user.username,
                                                 project.name,
                                                 self.object.sequence)
        self.queryset = self.model_class.objects.all()

        # Add 2 experiments
        for _ in range(2):
            ExperimentFactory(experiment_group=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data
        assert resp.data['num_pending_experiments'] == 2

    def test_patch(self):
        new_description = 'updated_xp_name'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description
        assert new_object.experiments.count() == 2

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert Experiment.objects.count() == 2
        with patch('libs.paths.experiments.delete_path') as outputs_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert outputs_mock_stop.call_count == 4  # Outputs and Logs * 2
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
        assert Experiment.objects.count() == 0


@pytest.mark.experiment_groups_mark
class TestStopExperimentGroupViewV1(BaseViewTest):
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        with patch('hpsearch.tasks.grid.hp_grid_search_start.apply_async') as mock_fct:
            self.object = self.factory_class(project=project)

        assert mock_fct.call_count == 1
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
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_stop_experiments.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1

        # Execute the function
        with patch('scheduler.experiment_scheduler.stop_experiment') as _:  # noqa
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_200_OK
        assert self.object.stopped_experiments.count() == 2

    def test_stop_pending(self):
        data = {'pending': True}
        assert self.object.stopped_experiments.count() == 0

        # Check that is calling the correct function
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_stop_experiments.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1

        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.stopped_experiments.count() == 2
