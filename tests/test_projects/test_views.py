from unittest.mock import patch

from flaky import flaky
from rest_framework import status

from django.test import override_settings, tag

from experiment_groups.models import ExperimentGroup
from experiments.models import Experiment
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_projects import ProjectFactory
from polyaxon.urls import API_V1
from projects.models import Project
from projects.serializers import ProjectDetailSerializer, ProjectSerializer
from tests.utils import RUNNER_TEST, BaseViewTest


class TestProjectCreateViewV1(BaseViewTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.url = '/{}/projects/'.format(API_V1)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        data = {'name': 'new_project'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1


class TestProjectListViewV1(BaseViewTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.user = self.auth_client.user
        self.url = '/{}/{}'.format(API_V1, self.user.username)
        self.objects = [self.factory_class(user=self.user) for _ in range(self.num_objects)]
        # Other user objetcs
        self.other_object = self.factory_class()
        # One private project
        self.private = self.factory_class(user=self.other_object.user, is_public=False)
        self.url_other = '/{}/{}'.format(API_V1, self.other_object.user)

        self.queryset = self.model_class.objects.filter(user=self.user)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_get_others(self):
        resp = self.auth_client.get(self.url_other)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 1

        data = resp.data['results']
        assert len(data) == 1
        assert data[0] == self.serializer_class(self.other_object).data

    @flaky(max_runs=3)
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


class TestProjectDetailViewV1(BaseViewTest):
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/{}/{}/'.format(API_V1, self.object.user.username, self.object.name)
        self.queryset = self.model_class.objects.filter(user=self.object.user)

        # Create related fields
        for _ in range(2):
            ExperimentGroupFactory(project=self.object)

        # creating the default factory should trigger the creation of 2 experiments per group
        assert Experiment.objects.count() == 4

        # Other user objects
        self.other_object = self.factory_class()
        self.url_other = '/{}/{}/{}/'.format(API_V1,
                                             self.other_object.user.username,
                                             self.other_object.name)
        # One private project
        self.private = self.factory_class(is_public=False)
        self.url_private = '/{}/{}/{}/'.format(API_V1,
                                               self.private.user.username,
                                               self.private.name)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert resp.data['num_experiments'] == 4
        assert resp.data['num_experiment_groups'] == 2

        # Get other public project works
        resp = self.auth_client.get(self.url_other)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.other_object).data

        # Get other private project does not work
        resp = self.auth_client.get(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

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
        assert new_object.experiments.count() == 4
        assert new_object.experiment_groups.count() == 2

        # Patch does not work for other project public and private
        resp = self.auth_client.delete(self.url_other)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        resp = self.auth_client.delete(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    @override_settings(DEPLOY_RUNNER=False)
    def test_delete(self):
        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 4

        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as xp_mock_stop:
            with patch('projects.paths.delete_path') as delete_path_project_mock_stop:
                with patch('experiment_groups.paths.delete_path') as delete_path_group_mock_stop:
                    with patch('experiments.paths.delete_path') as delete_path_xp_mock_stop:
                        resp = self.auth_client.delete(self.url)
        assert xp_mock_stop.call_count == 4
        # 2 * project + 1 repo
        assert delete_path_project_mock_stop.call_count == 3
        # 2 * 2 * groups
        assert delete_path_group_mock_stop.call_count
        assert delete_path_xp_mock_stop.call_count == 8  # 2 * 4  * groups
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert Experiment.objects.count() == 0

        # Delete does not work for other project public and private
        resp = self.auth_client.delete(self.url_other)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        resp = self.auth_client.delete(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    @tag(RUNNER_TEST)
    def test_delete_runner(self):
        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 4
        with patch('runner.schedulers.tensorboard_scheduler.'
                   'stop_tensorboard') as tensorboard_mock_fct:
            with patch('runner.schedulers.notebook_scheduler.'
                       'stop_notebook') as notebook_mock_fct:
                with patch('runner.schedulers.experiment_scheduler.'
                           'stop_experiment') as xp_mock_stop:
                    with patch('projects.paths.delete_path') as delete_path_project_mock_stop:
                        with patch('experiment_groups.paths.'
                                   'delete_path') as delete_path_group_mock_stop:
                            with patch('experiments.paths.delete_path') as delete_path_xp_mock_stop:
                                resp = self.auth_client.delete(self.url)
        assert xp_mock_stop.call_count == 4
        assert tensorboard_mock_fct.call_count == 1
        assert notebook_mock_fct.call_count == 1
        # 2 * project + 1 repo
        assert delete_path_project_mock_stop.call_count == 3
        # 2 * 2 * groups
        assert delete_path_group_mock_stop.call_count
        assert delete_path_xp_mock_stop.call_count == 8  # 2 * 4  * groups
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert Experiment.objects.count() == 0

        # Delete does not work for other project public and private
        resp = self.auth_client.delete(self.url_other)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        resp = self.auth_client.delete(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
