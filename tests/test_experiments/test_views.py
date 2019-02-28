# pylint:disable=too-many-lines
import os
import time

from faker import Faker
from unittest.mock import patch

import pytest

from hestia.internal_services import InternalServices
from rest_framework import status

import conf
import stores

from api.code_reference.serializers import CodeReferenceSerializer
from api.experiments import queries
from api.experiments.serializers import (
    BookmarkedExperimentSerializer,
    ExperimentChartViewSerializer,
    ExperimentDeclarationsSerializer,
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
    ExperimentLastMetricSerializer,
    ExperimentMetricSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from api.utils.views.protected import ProtectedView
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.bookmarks import Bookmark
from db.models.experiment_groups import GroupTypes
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import (
    Experiment,
    ExperimentChartView,
    ExperimentMetric,
    ExperimentStatus
)
from db.models.repos import CodeReference
from db.redis.ephemeral_tokens import RedisEphemeralTokens
from db.redis.group_check import GroupChecks
from db.redis.heartbeat import RedisHeartBeat
from db.redis.tll import RedisTTL
from factories.factory_code_reference import CodeReferenceFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import (
    ExperimentChartViewFactory,
    ExperimentFactory,
    ExperimentJobFactory,
    ExperimentJobStatusFactory,
    ExperimentMetricFactory,
    ExperimentStatusFactory
)
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import (
    exec_experiment_outputs_refs_parsed_content,
    exec_experiment_spec_parsed_content,
    exec_experiment_resources_parsed_content)
from schemas.specifications import ExperimentSpecification
from tests.utils import BaseFilesViewTest, BaseViewTest, EphemeralClient


@pytest.mark.experiments_mark
class TestProjectExperimentListViewV1(BaseViewTest):
    serializer_class = BookmarkedExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/experiments/'.format(API_V1,
                                                   self.project.user.username,
                                                   self.project.name)
        self.other_url = '/{}/{}/{}/experiments/'.format(API_V1,
                                                         self.other_project.user.username,
                                                         self.other_project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.other_object = self.factory_class(project=self.other_project)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Test other
        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK

        independent_count = self.queryset.count()
        # Create group to test independent filter
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as mock_fct:
            group = ExperimentGroupFactory(project=self.project)
        assert mock_fct.call_count == 1
        [self.factory_class(project=self.project, experiment_group=group) for _ in range(2)]  # noqa
        all_experiment_count = self.queryset.all().count()
        assert all_experiment_count == independent_count + group.experiments.count()

        # Getting all experiments
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == all_experiment_count

        # Getting only independent experiments
        resp = self.auth_client.get(self.url + '?independent=true')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == independent_count
        # Through query
        resp = self.auth_client.get(self.url + '?query=independent:true')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == independent_count

        # Getting only group experiments
        resp = self.auth_client.get(self.url + '?group={}'.format(group.id))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == group.experiments.count()

        # Filtering for independent and group experiments should raise
        resp = self.auth_client.get(self.url + '?independent=true&group={}'.format(group.id))
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_with_bookmarked_objects(self):
        # Other user bookmark
        Bookmark.objects.create(
            user=self.other_project.user,
            content_object=self.objects[0])

        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(len([1 for obj in resp.data['results'] if obj['bookmarked'] is True]), 0)

        # Authenticated user bookmark
        Bookmark.objects.create(
            user=self.auth_client.user,
            content_object=self.objects[0])

        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert len([1 for obj in resp.data['results'] if obj['bookmarked'] is True]) == 1

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

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '?sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

        resp = self.auth_client.get(self.url + '?sort=-started_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset.order_by('-started_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_get_filter(self):
        # Wrong filter raises
        resp = self.auth_client.get(self.url + '?query=created_at<2010-01-01')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        resp = self.auth_client.get(self.url + '?query=created_at:<2010-01-01')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:Finished')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:created|running')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Id
        resp = self.auth_client.get(self.url +
                                    '?query=id:{}|{}'.format(self.objects[0].id,
                                                             self.objects[1].id))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['next'] is None
        assert resp.data['count'] == 2

        # Name
        self.objects[0].name = 'exp_foo'
        self.objects[0].save()

        resp = self.auth_client.get(self.url +
                                    '?query=name:exp_foo')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['next'] is None
        assert resp.data['count'] == 1

        resp = self.auth_client.get(self.url +
                                    '?query=project.name:{}'.format(self.project.name))
        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        # Set metrics
        optimizers = ['sgd', 'sgd', 'adam']
        tags = [['tag1'], ['tag1', 'tag2'], ['tag2']]
        losses = [0.1, 0.2, 0.9]
        for i, obj in enumerate(self.objects[:3]):
            ExperimentMetricFactory(experiment=obj, values={'loss': losses[i]})
            obj.declarations = {'optimizer': optimizers[i]}
            obj.tags = tags[i]
            obj.save()

        resp = self.auth_client.get(
            self.url + '?query=created_at:>=2010-01-01,'
                       'declarations.optimizer:sgd,'
                       'metric.loss:>=0.2,'
                       'tags:tag1')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 1

        resp = self.auth_client.get(
            self.url + '?query=created_at:>=2010-01-01,'
                       'declarations.optimizer:sgd|adam,'
                       'metric.loss:>=0.2,'
                       'tags:tag1|tag2')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 2

        # Order by metrics
        resp = self.auth_client.get(self.url + '?sort=-metric.loss')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == [self.serializer_class(obj).data for obj in reversed(self.objects)]

        resp = self.auth_client.get(self.url + '?sort=metric.loss')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == [self.serializer_class(obj).data for obj in self.objects]

    def test_get_filter_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(
            self.url,
            limit,
            '?query=created_at:>=2010-01-01,status:created|running'))
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

    def test_create_ttl(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Experiment.objects.last()
        assert RedisTTL.get_for_experiment(xp.id) == conf.get('GLOBAL_COUNTDOWN')

        data = {'ttl': 10}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Experiment.objects.last()
        assert RedisTTL.get_for_experiment(xp.id) == 10

        data = {'ttl': 'foo'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_in_cluster(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Experiment.objects.last()
        assert xp.in_cluster is True
        assert xp.run_env is None

        data = {'in_cluster': False, 'run_env': {'foo': 'bar'}}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Experiment.objects.last()
        assert xp.in_cluster is False
        assert xp.run_env == {'foo': 'bar'}

    def test_create(self):
        data = {'check_specification': True}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': exec_experiment_spec_parsed_content.parsed_data}
        resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_create_with_runner(self):
        data = {'check_specification': True}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': exec_experiment_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_create_with_outputs_refs(self):
        data = {'config': exec_experiment_outputs_refs_parsed_content.parsed_data}
        resp = self.auth_client.post(self.url, data)
        # No job refs
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Creating the job should pass
        JobFactory(project=self.project, name='foo')  # noqa
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == self.num_objects + 1
        experiment = self.queryset.order_by('created_at').last()
        assert experiment.outputs_refs is not None
        assert len(experiment.outputs_refs_jobs) == 1
        assert experiment.outputs_refs_experiments is None
        assert len(experiment.outputs_jobs) == 1
        assert experiment.outputs_experiments is None

    def test_create_without_config_passes_if_no_spec_validation_requested(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.config is None

    def test_create_with_declarations(self):
        data = {
            'declarations': {
                'lr': 0.1,
                'dropout': 0.5
            }
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.config is None
        assert last_object.declarations == {
            'lr': 0.1,
            'dropout': 0.5
        }

    def test_create_in_group(self):
        # Create in wrong group raises
        group = ExperimentGroupFactory()
        assert group.experiments.count() == 0

        data = {
            'declarations': {
                'lr': 0.1,
                'dropout': 0.5
            },
            'experiment_group': group.id
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Create in correct group passes
        group = ExperimentGroupFactory(project=self.project)
        assert group.experiments.count() == 0

        data = {
            'declarations': {
                'lr': 0.1,
                'dropout': 0.5
            },
            'experiment_group': group.id
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert group.experiments.count() == 1

    def test_create_in_selection(self):
        # Create in wrong selection raises
        group = ExperimentGroupFactory(group_type=GroupTypes.SELECTION, content=None)
        assert group.experiments.count() == 0

        data = {
            'declarations': {
                'lr': 0.1,
                'dropout': 0.5
            },
            'experiment_group': group.id
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Create in correct group passes
        group = ExperimentGroupFactory(project=self.project,
                                       group_type=GroupTypes.SELECTION,
                                       content=None)
        assert group.experiments.count() == 0
        assert group.selection_experiments.count() == 0

        data = {
            'declarations': {
                'lr': 0.1,
                'dropout': 0.5
            },
            'experiment_group': group.id
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert group.selection_experiments.count() == 1


@pytest.mark.experiments_mark
class TestProjectExperimentLastMetricListViewV1(BaseViewTest):
    metrics_serializer_class = ExperimentLastMetricSerializer
    declarations_serializer_class = ExperimentDeclarationsSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/experiments/'.format(API_V1,
                                                   self.project.user.username,
                                                   self.project.name)
        self.objects = [self.factory_class(project=self.project,
                                           declarations={'param1': i, 'param2': i * 2})
                        for i in range(self.num_objects)]
        # Create Metrics
        for obj in self.objects:
            ExperimentMetricFactory(experiment=obj)
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get_metrics(self):
        resp = self.auth_client.get(self.url + '?metrics=true')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == self.queryset.count()
        assert resp.data['results'] == self.metrics_serializer_class(
            self.queryset, many=True).data

    def test_get_declarations(self):
        resp = self.auth_client.get(self.url + '?declarations=true')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == self.queryset.count()
        assert resp.data['results'] == self.declarations_serializer_class(
            self.queryset, many=True).data

    def test_get_all(self):
        Experiment.objects.bulk_create([
            Experiment(project=self.project, user=self.auth_client.user)
            for _ in range(30)
        ])
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == self.queryset.count()
        assert len(resp.data['results']) < self.queryset.count()

        resp = self.auth_client.get(self.url + '?all=true')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == self.queryset.count()
        assert len(resp.data['results']) == self.queryset.count()


@pytest.mark.experiments_mark
class TestExperimentGroupExperimentListViewV1(BaseViewTest):
    serializer_class = BookmarkedExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.experiment_group = ExperimentGroupFactory(project=self.project)
        self.objects = [self.factory_class(project=self.project,
                                           experiment_group=self.experiment_group)
                        for _ in range(self.num_objects)]
        self.url = '/{}/{}/{}/experiments?group={}'.format(
            API_V1,
            self.experiment_group.project.user,
            self.experiment_group.project.name,
            self.experiment_group.id)
        # one object that does not belong to the filter
        self.factory_class(project=self.experiment_group.project)
        self.queryset = self.model_class.objects.filter(experiment_group=self.experiment_group)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}".format(self.url, limit))
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

    def test_pagination_all(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}".format(self.url, limit))
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

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '&sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data


@pytest.mark.experiments_mark
class TestExperimentSelectionListViewV1(BaseViewTest):
    serializer_class = BookmarkedExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.experiment_group = ExperimentGroupFactory(project=self.project,
                                                       content=None,
                                                       group_type=GroupTypes.SELECTION)
        self.objects = [self.factory_class(project=self.project)
                        for _ in range(self.num_objects)]
        self.experiment_group.selection_experiments.set(self.objects)
        self.url = '/{}/{}/{}/experiments?group={}'.format(
            API_V1,
            self.experiment_group.project.user,
            self.experiment_group.project.name,
            self.experiment_group.id)
        # one object that does not belong to the filter
        self.factory_class(project=self.experiment_group.project)
        self.queryset = self.experiment_group.selection_experiments.all()
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}".format(self.url, limit))
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

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '&sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data


@pytest.mark.experiments_mark
class TestRunnerExperimentGroupExperimentListViewV1(BaseViewTest):
    serializer_class = BookmarkedExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_EXECUTOR = False
    DISABLE_RUNNER = False

    def setUp(self):
        super().setUp()
        content = """---
    version: 1

    kind: group

    hptuning:
      matrix:
        lr:
          linspace: '1.:3.:3'

    model:
      model_type: regressor
      loss:
        MeanSquaredError:
      optimizer:
        Adam:
          learning_rate: "{{ lr }}"
      graph:
        input_layers: images
        layers:
          - Conv2D:
              filters: 64
              kernel_size: [3, 3]
              strides: [1, 1]
              activation: relu
              kernel_initializer: Ones
          - MaxPooling2D:
              kernels: 2
          - Flatten:
          - Dense:
              units: 10
              activation: softmax

    train:
      data_pipeline:
        TFRecordImagePipeline:
          batch_size: 64
          num_epochs: 1
          shuffle: true
          dynamic_pad: false
          data_files: ["../data/mnist/mnist_train.tfrecord"]
          meta_data_file: "../data/mnist/meta_data.json"
"""
        self.project = ProjectFactory()
        with patch.object(GroupChecks, 'is_checked') as mock_is_check:
            with patch('hpsearch.tasks.grid.hp_grid_search_start.retry') as start_fct:
                with patch('scheduler.tasks.experiments.'
                           'experiments_build.apply_async') as build_fct:
                    mock_is_check.return_value = False
                    self.experiment_group = ExperimentGroupFactory(
                        project=self.project,
                        content=content)

        assert start_fct.call_count == 1
        assert build_fct.call_count == 2
        assert self.experiment_group.specification.matrix_space == 3
        self.url = '/{}/{}/{}/experiments?group={}'.format(
            API_V1,
            self.experiment_group.project.user,
            self.experiment_group.project.name,
            self.experiment_group.id)
        # one object that does not belong to the filter
        self.factory_class(project=self.project)
        self.queryset = self.model_class.objects.filter(experiment_group=self.experiment_group)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}".format(self.url, limit))
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

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '&sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.num_objects

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}&limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data


@pytest.mark.experiments_mark
class TestExperimentDetailViewV1(BaseViewTest):
    serializer_class = ExperimentDetailSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True
    DISABLE_RUNNER = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as spawner_mock_start:
            self.object = self.factory_class(project=project)
        assert spawner_mock_start.call_count == 1
        self.url = '/{}/{}/{}/experiments/{}/'.format(API_V1,
                                                      project.user.username,
                                                      project.name,
                                                      self.object.id)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for _ in range(2):
            ExperimentJobFactory(experiment=self.object)

        self.object_query = queries.experiments_details.get(id=self.object.id)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object_query).data
        assert resp.data['num_jobs'] == 2

    def test_get_with_resource_reg_90(self):
        # Fix issue#90:
        # Failed to getting experiment when specify resources without framework in environment
        spec_content = """---
            version: 1

            kind: experiment

            environment:
              node_selector: 
                foo: bar
              tolerations:
                - key: "key"
                  operator: "Equal"
                  value: "value"
                  effect: "NoSchedule"
              affinity:
                foo: bar
              resources:
                gpu:
                  requests: 1
                  limits: 1
                tpu:
                  requests: 1
                  limits: 1

            build:
              image: my_image

            run:
              cmd: video_prediction_train --model=DNA --num_masks=1
        """
        spec_parsed_content = ExperimentSpecification.read(spec_content)

        project = ProjectFactory(user=self.auth_client.user)
        exp = self.factory_class(project=project, config=spec_parsed_content.parsed_data)
        url = '/{}/{}/{}/experiments/{}/'.format(API_V1,
                                                 project.user.username,
                                                 project.name,
                                                 exp.id)

        resp = self.auth_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        exp_query = queries.experiments_details.get(id=exp.id)
        assert resp.data == self.serializer_class(exp_query).data

    def test_patch_exp(self):  # pylint:disable=too-many-statements
        new_description = 'updated_xp_name'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description
        assert new_object.jobs.count() == 2

        # path in_cluster
        data = {'in_cluster': False}
        assert self.object.in_cluster is True
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.jobs.count() == 2
        assert new_object.in_cluster is False

        # path in_cluster
        data = {'in_cluster': None}
        assert new_object.in_cluster is False
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.jobs.count() == 2
        assert new_object.in_cluster is True

        # path in_cluster
        data = {'in_cluster': False}
        assert new_object.in_cluster is True
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.jobs.count() == 2
        assert new_object.in_cluster is False

        data = {'in_cluster': True}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.jobs.count() == 2
        assert new_object.in_cluster is True

        # Update original experiment
        assert new_object.is_clone is False
        new_experiment = ExperimentFactory()
        data = {'original_experiment': new_experiment.id}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description == new_description
        assert new_object.jobs.count() == 2
        assert new_object.is_clone is True
        assert new_object.original_experiment == new_experiment

        # Update tags
        assert new_object.tags == ['fixtures']
        data = {'tags': ['foo', 'bar']}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert sorted(new_object.tags) == sorted(['foo', 'bar'])

        data = {'tags': ['foo_new', 'bar_new'], 'merge': False}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert sorted(new_object.tags) == sorted(['foo_new', 'bar_new'])

        data = {'tags': ['foo', 'bar'], 'merge': True}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert sorted(new_object.tags) == sorted(['foo_new', 'bar_new', 'foo', 'bar'])

        # Update declarations
        assert new_object.declarations is None
        data = {'declarations': {'foo': 'bar'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.declarations == {'foo': 'bar'}

        data = {'declarations': {'foo_new': 'bar_new'}, 'merge': False}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.declarations == {'foo_new': 'bar_new'}

        data = {'declarations': {'foo': 'bar'}, 'merge': True}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.declarations == {'foo_new': 'bar_new', 'foo': 'bar'}

        # Update name
        data = {'name': 'new_name'}
        assert new_object.name is None
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']

    def test_delete_from_created_status_archives_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        with patch('scheduler.experiment_scheduler.stop_experiment') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Deleted
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0
        assert ExperimentJob.objects.count() == 0

    def test_delete_from_running_status_archives_and_schedules_stop(self):
        self.object.set_status(ExperimentLifeCycle.RUNNING)
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        with patch('scheduler.experiment_scheduler.stop_experiment') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Deleted
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0
        assert ExperimentJob.objects.count() == 0

    def test_delete_archives_and_schedules_deletion(self):
        self.object.set_status(ExperimentLifeCycle.RUNNING)
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        with patch('scheduler.tasks.experiments.'
                   'experiments_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Patched
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        assert ExperimentJob.objects.count() == 2

    def test_archive_schedule_deletion(self):
        self.object.set_status(ExperimentLifeCycle.RUNNING)
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        with patch('scheduler.tasks.experiments.'
                   'experiments_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_archive_schedule_archives_and_schedules_stop(self):
        self.object.set_status(ExperimentLifeCycle.RUNNING)
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        with patch('scheduler.tasks.experiments.'
                   'experiments_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        assert ExperimentJob.objects.count() == 2

    def test_restore(self):
        self.object.archive()
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        resp = self.auth_client.post(self.url + 'restore/')
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1
        assert ExperimentJob.objects.count() == 2


@pytest.mark.experiments_mark
class TestExperimentCodeReferenceViewV1(BaseViewTest):
    serializer_class = CodeReferenceSerializer
    model_class = CodeReference
    factory_class = CodeReferenceFactory

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/coderef/'.format(API_V1,
                                                              project.user.username,
                                                              project.name,
                                                              self.experiment.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        coderef = CodeReferenceFactory()
        self.experiment.code_reference = coderef
        self.experiment.save()
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(coderef).data

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == 1
        last_object = self.model_class.objects.last()
        self.experiment.refresh_from_db()
        assert last_object == self.experiment.code_reference
        assert last_object.branch == 'master'
        assert last_object.commit is None
        assert last_object.head is None
        assert last_object.is_dirty is False
        assert last_object.git_url is None
        assert last_object.repo is None
        assert last_object.external_repo is None

        data = {
            'commit': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'head': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'branch': 'feature1',
            'git_url': 'https://bitbucket.org:foo/bar.git',
            'is_dirty': True
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == 2
        last_object = self.model_class.objects.last()
        self.experiment.refresh_from_db()
        assert last_object == self.experiment.code_reference
        assert last_object.branch == 'feature1'
        assert last_object.commit == '3783ab36703b14b91b15736fe4302bfb8d52af1c'
        assert last_object.head == '3783ab36703b14b91b15736fe4302bfb8d52af1c'
        assert last_object.is_dirty is True
        assert last_object.git_url == 'https://bitbucket.org:foo/bar.git'
        assert last_object.repo is None
        assert last_object.external_repo is None


@pytest.mark.experiments_mark
class TestExperimentStatusListViewV1(BaseViewTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
            with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/statuses/'.format(API_V1,
                                                               project.user.username,
                                                               project.name,
                                                               self.experiment.id)
        self.objects = [self.factory_class(experiment=self.experiment,
                                           status=ExperimentLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('created_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        resp = self.internal_client.get(self.url)
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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.status == ExperimentLifeCycle.CREATED

        data = {'status': ExperimentLifeCycle.RUNNING}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.status == data['status']

        # Create with message and traceback
        data = {'status': ExperimentLifeCycle.FAILED,
                'message': 'message1',
                'traceback': 'traceback1'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 3
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']

        # Test internal
        data = {}
        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 4


@pytest.mark.experiments_mark
class TestExperimentMetricListViewV1(BaseViewTest):
    serializer_class = ExperimentMetricSerializer
    model_class = ExperimentMetric
    factory_class = ExperimentMetricFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/metrics/'.format(API_V1,
                                                              project.user.username,
                                                              project.name,
                                                              self.experiment.id)
        self.objects = [self.factory_class(experiment=self.experiment, values={'accuracy': i / 10})
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('created_at')

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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'values': {'precision': 0.9}}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.values == data['values']

    def test_create_many(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = [
            {'values': {'precision': 0.9}},
            {'values': {'precision': 0.95}},
            {'values': {'precision': 0.99}}
        ]
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 3
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.values == data[-1]['values']

        with patch('scheduler.tasks.experiments.experiments_set_metrics.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1

    def test_create_internal(self):
        data = {}
        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'values': {'precision': 0.9}}
        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.values == data['values']


@pytest.mark.experiments_mark
class TestExperimentStatusDetailViewV1(BaseViewTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:  # noqa
            with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
                self.experiment = ExperimentFactory()
        self.object = self.factory_class(experiment=self.experiment)
        self.url = '/{}/{}/{}/experiments/{}/statuses/{}/'.format(
            API_V1,
            self.experiment.project.user.username,
            self.experiment.project.name,
            self.experiment.id,
            self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'status': ExperimentLifeCycle.SUCCEEDED}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.model_class.objects.count() == 1


@pytest.mark.experiments_mark
class TestExperimentJobListViewV1(BaseViewTest):
    serializer_class = ExperimentJobSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/jobs/'.format(
            API_V1,
            project.user.username,
            project.name,
            self.experiment.id)
        self.objects = [self.factory_class(experiment=self.experiment)
                        for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('-updated_at')

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

    def test_create(self):
        data = {'definition': {'key': 'my new kob k8s'}}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.definition == data['definition']


@pytest.mark.experiments_mark
class TestExperimentJobDetailViewV1(BaseViewTest):
    serializer_class = ExperimentJobDetailSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.object = self.factory_class(experiment=self.experiment)
        self.url = '/{}/{}/{}/experiments/{}/jobs/{}/'.format(
            API_V1,
            project.user.username,
            project.name,
            self.experiment.id,
            self.object.id)
        self.queryset = self.model_class.objects.filter(experiment=self.experiment)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'definition': {'new_key': 'new_value'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.experiment == self.object.experiment
        assert new_object.definition != self.object.definition
        assert new_object.definition == data['definition']

    def test_cannot_path_experiment(self):
        data = {'experiment': ExperimentFactory().id}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.experiment == self.object.experiment

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0


@pytest.mark.experiments_mark
class TestExperimentJobStatusListViewV1(BaseViewTest):
    serializer_class = ExperimentJobStatusSerializer
    model_class = ExperimentJobStatus
    factory_class = ExperimentJobStatusFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            with patch.object(ExperimentJob, 'set_status') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                experiment = ExperimentFactory(project=project)
                self.experiment_job = ExperimentJobFactory(experiment=experiment)
        self.url = '/{}/{}/{}/experiments/{}/jobs/{}/statuses/'.format(
            API_V1,
            project.user.username,
            project.name,
            experiment.id,
            self.experiment_job.id)
        self.objects = [self.factory_class(job=self.experiment_job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter(job=self.experiment_job)
        self.queryset = self.queryset.order_by('created_at')

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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.status == JobLifeCycle.CREATED

        data = {'status': JobLifeCycle.SUCCEEDED}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.job == self.experiment_job
        assert last_object.status == data['status']


@pytest.mark.experiments_mark
class TestExperimentJobStatusDetailViewV1(BaseViewTest):
    serializer_class = ExperimentJobStatusSerializer
    model_class = ExperimentJobStatus
    factory_class = ExperimentJobStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            with patch.object(ExperimentJob, 'set_status') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                experiment = ExperimentFactory(project=project)
                self.experiment_job = ExperimentJobFactory(experiment=experiment)
                self.object = self.factory_class(job=self.experiment_job)
        self.url = '/{}/{}/{}/experiments/{}/jobs/{}/statuses/{}'.format(
            API_V1,
            project.user.username,
            project.name,
            experiment.id,
            self.experiment_job.id,
            self.object.uuid.hex)
        self.queryset = self.model_class.objects.filter(job=self.experiment_job)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'details': {'message': 'bla', 'reason': 'some reason'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.details == {}
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.details == {'message': 'bla', 'reason': 'some reason'}

        data = {'message': 'new reason', 'details': {'message': 'bla2', 'reason': 'some reason3'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.message == 'new reason'
        assert new_object.details == {'message': 'bla2', 'reason': 'some reason3'}

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.model_class.objects.count() == 1


@pytest.mark.experiments_mark
class TestExperimentJobLogsViewV1(BaseViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(
            project=project,
            config=exec_experiment_resources_parsed_content.parsed_data)
        self.experiment_job = ExperimentJobFactory(experiment=self.experiment)
        self.logs = []
        self.url = '/{}/{}/{}/experiments/{}/jobs/{}/logs'.format(
            API_V1,
            project.user.username,
            project.name,
            self.experiment.id,
            self.experiment_job.id)

    def create_logs(self, temp):
        log_path = stores.get_experiment_job_logs_path(
            experiment_job_name=self.experiment_job.unique_name,
            temp=temp)
        stores.create_experiment_job_logs_path(experiment_job_name=self.experiment_job.unique_name,
                                               temp=temp)
        fake = Faker()
        self.logs = []
        for _ in range(self.num_log_lines):
            self.logs.append(fake.sentence())
        with open(log_path, 'w') as file:
            for line in self.logs:
                file.write(line)
                file.write('\n')

    def test_get_done_experiment(self):
        self.experiment.set_status(ExperimentLifeCycle.SUCCEEDED)
        self.assertTrue(self.experiment.is_done)
        # No logs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check the it does not return temp file
        self.create_logs(temp=True)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check returns the correct file
        self.create_logs(temp=False)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs

    @patch('api.experiments.views.process_experiment_job_logs')
    def test_get_non_done_experiment(self, _):
        self.assertFalse(self.experiment.is_done)
        # No logs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check the it does not return non temp file
        self.create_logs(temp=False)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check returns the correct file
        self.create_logs(temp=True)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs


@pytest.mark.experiments_mark
class TestRestartExperimentViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True
    DISABLE_RUNNER = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/restart'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_restart(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2

        last_experiment = self.queryset.last()
        assert last_experiment.is_clone is True
        assert last_experiment.is_restart is True
        assert last_experiment.is_copy is False
        assert last_experiment.is_resume is False
        assert last_experiment.original_experiment == self.object
        assert last_experiment.original_unique_name == self.object.unique_name

    def test_restart_patch_config(self):
        data = {'config': {'declarations': {'lr': 0.1}}}
        assert self.queryset.first().declarations is None
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2
        assert self.queryset.first().declarations is None
        assert self.queryset.last().declarations == data['config']['declarations']

        last_experiment = self.queryset.last()
        assert last_experiment.is_clone is True
        assert last_experiment.is_restart is True
        assert last_experiment.is_copy is False
        assert last_experiment.is_resume is False
        assert last_experiment.original_experiment == self.object
        assert last_experiment.original_unique_name == self.object.unique_name

    def test_restart_patch_wrong_config_raises(self):
        data = {'config': {'lr': 0.1}}
        assert self.queryset.first().declarations is None
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert mock_fct.call_count == 0
        assert self.queryset.count() == 1


@pytest.mark.experiments_mark
class TestResumeExperimentViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/resume'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_resume(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2

        last_experiment = self.queryset.last()
        assert last_experiment.is_clone is True
        assert last_experiment.is_restart is False
        assert last_experiment.is_copy is False
        assert last_experiment.is_resume is True
        assert last_experiment.original_experiment == self.object
        assert last_experiment.original_unique_name == self.object.unique_name

    def test_resume_patch_config(self):
        data = {'config': {'declarations': {'lr': 0.1}}}
        assert self.queryset.first().declarations is None
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2
        assert self.queryset.first().declarations is None
        assert self.queryset.last().declarations == data['config']['declarations']

        last_experiment = self.queryset.last()
        assert last_experiment.is_clone is True
        assert last_experiment.is_restart is False
        assert last_experiment.is_copy is False
        assert last_experiment.is_resume is True
        assert last_experiment.original_experiment == self.object
        assert last_experiment.original_unique_name == self.object.unique_name

    def test_resume_patch_wrong_config_raises(self):
        data = {'config': {'lr': 0.1}}
        assert self.queryset.first().declarations is None
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert mock_fct.call_count == 0
        assert self.queryset.count() == 1


@pytest.mark.experiments_mark
class TestCopyExperimentViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True
    DISABLE_RUNNER = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/copy'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_resume(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2

        last_experiment = self.queryset.last()
        assert last_experiment.is_clone is True
        assert last_experiment.is_restart is False
        assert last_experiment.is_copy is True
        assert last_experiment.is_resume is False
        assert last_experiment.original_experiment == self.object
        assert last_experiment.original_unique_name == self.object.unique_name

    def test_resume_patch_config(self):
        data = {'config': {'declarations': {'lr': 0.1}}}
        assert self.queryset.first().declarations is None
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2
        assert self.queryset.first().declarations is None
        assert self.queryset.last().declarations == data['config']['declarations']

        last_experiment = self.queryset.last()
        assert last_experiment.is_clone is True
        assert last_experiment.is_restart is False
        assert last_experiment.is_copy is True
        assert last_experiment.is_resume is False
        assert last_experiment.original_experiment == self.object
        assert last_experiment.original_unique_name == self.object.unique_name

    def test_resume_patch_wrong_config_raises(self):
        data = {'config': {'lr': 0.1}}
        assert self.queryset.first().declarations is None
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert mock_fct.call_count == 0
        assert self.queryset.count() == 1


@pytest.mark.experiments_mark
class TestStopExperimentViewV1(BaseViewTest):
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/stop'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.experiments_mark
class TestStopExperimentManyViewV1(BaseViewTest):
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.objects = [self.factory_class(project=project) for _ in range(3)]
        self.url = '/{}/{}/{}/experiments/stop'.format(
            API_V1,
            project.user.username,
            project.name)
        self.queryset = self.model_class.objects.all()

    def test_stop_many(self):
        data = {}
        assert self.queryset.count() == 3
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 0

        data = {'ids': [obj.id for obj in self.objects]}
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 3
        assert self.queryset.count() == 3


@pytest.mark.experiments_mark
class TestDeleteExperimentManyViewV1(BaseViewTest):
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.objects = [self.factory_class(project=project) for _ in range(3)]
        self.url = '/{}/{}/{}/experiments/delete'.format(
            API_V1,
            project.user.username,
            project.name)
        self.queryset = self.model_class.objects.all()

    def test_delete_many(self):
        data = {}
        assert self.queryset.count() == 3
        resp = self.auth_client.delete(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 3

        data = {'ids': [obj.id for obj in self.objects]}
        resp = self.auth_client.delete(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0


@pytest.mark.experiments_mark
class TestExperimentLogsViewV1(BaseViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.logs = []
        self.url = '/{}/{}/{}/experiments/{}/logs'.format(
            API_V1,
            project.user.username,
            project.name,
            self.experiment.id)

    def create_logs(self, temp):
        log_path = stores.get_experiment_logs_path(
            experiment_name=self.experiment.unique_name,
            temp=temp)
        stores.create_experiment_logs_path(experiment_name=self.experiment.unique_name, temp=temp)
        fake = Faker()
        self.logs = []
        for _ in range(self.num_log_lines):
            self.logs.append(fake.sentence())
        with open(log_path, 'w') as file:
            for line in self.logs:
                file.write(line)
                file.write('\n')

    def test_get_done_experiment(self):
        self.experiment.set_status(ExperimentLifeCycle.SUCCEEDED)
        self.assertTrue(self.experiment.is_done)
        # No logs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check the it does not return temp file
        self.create_logs(temp=True)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check returns the correct file
        self.create_logs(temp=False)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs

    @patch('api.experiments.views.process_logs')
    def test_get_non_done_experiment(self, _):
        self.assertFalse(self.experiment.is_done)
        # No logs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check the it does not return non temp file
        self.create_logs(temp=False)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check returns the correct file
        self.create_logs(temp=True)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs

    def test_post_logs(self):
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = 'logs here'
        with patch('logs_handlers.tasks.logs_handle_experiment_job.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1

        data = ['logs here', 'dfg dfg']
        with patch('logs_handlers.tasks.logs_handle_experiment_job.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1


@pytest.mark.experiments_mark
class TestExperimentOutputsTreeViewV1(BaseFilesViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/outputs/tree'.format(
            API_V1,
            project.user.username,
            project.name,
            experiment.id)

        outputs_path = stores.get_experiment_outputs_path(
            persistence=experiment.persistence_outputs,
            experiment_name=experiment.unique_name,
            original_name=experiment.original_unique_name,
            cloning_strategy=experiment.cloning_strategy)
        stores.create_experiment_outputs_path(
            persistence=experiment.persistence_outputs,
            experiment_name=experiment.unique_name)

        self.create_paths(path=outputs_path, url=self.url)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assert_same_content(resp.data['files'], self.top_level['files'])
        self.assert_same_content(resp.data['dirs'], self.top_level['dirs'])

        resp = self.auth_client.get(self.url_second_level)
        assert resp.status_code == status.HTTP_200_OK
        self.assert_same_content(resp.data['files'], self.second_level['files'])
        self.assert_same_content(resp.data['dirs'], self.second_level['dirs'])

        resp = self.auth_client.get(self.url_second_level2)
        assert resp.status_code == status.HTTP_200_OK
        self.assert_same_content(resp.data['files'], self.second_level['files'])
        self.assert_same_content(resp.data['dirs'], self.second_level['dirs'])


@pytest.mark.experiments_mark
class TestExperimentOutputsFilesViewV1(BaseFilesViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/outputs/files'.format(
            API_V1,
            project.user.username,
            project.name,
            experiment.id)

        outputs_path = stores.get_experiment_outputs_path(
            persistence=experiment.persistence_outputs,
            experiment_name=experiment.unique_name,
            original_name=experiment.original_unique_name,
            cloning_strategy=experiment.cloning_strategy)
        stores.create_experiment_outputs_path(
            persistence=experiment.persistence_outputs,
            experiment_name=experiment.unique_name)
        self.create_paths(path=outputs_path, url=self.url)

    def test_get(self):
        for file_content in self.top_level_files:
            resp = self.auth_client.get(self.url + '?path={}'.format(file_content['file']))
            assert resp.status_code == status.HTTP_200_OK
            data = [i for i in resp._iterator]  # pylint:disable=protected-access
            assert data[0].decode('utf-8') == file_content['data']

        for file_content in self.second_level_files:
            resp = self.auth_client.get(self.url + '?path={}'.format(file_content['file']))
            assert resp.status_code == status.HTTP_200_OK
            data = [i for i in resp._iterator]  # pylint:disable=protected-access
            assert data[0].decode('utf-8') == file_content['data']


@pytest.mark.experiments_mark
class DownloadExperimentOutputsViewTest(BaseViewTest):
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True
    HAS_INTERNAL = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.experiment = self.factory_class(project=self.project)
        self.download_url = '/{}/{}/{}/experiments/{}/outputs/download'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.experiment.id)
        self.experiment_outputs_path = stores.get_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name)
        self.url = self.download_url

    def create_tmp_outputs(self):
        stores.create_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name)
        for i in range(4):
            open('{}/{}'.format(self.experiment_outputs_path, i), '+w')

    def test_redirects_nginx_to_file(self):
        self.create_tmp_outputs()
        # Assert that the experiment outputs
        self.assertTrue(os.path.exists(self.experiment_outputs_path))
        response = self.auth_client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER],
                         '{}/{}.tar.gz'.format(conf.get('OUTPUTS_ARCHIVE_ROOT'),
                                               self.experiment.unique_name.replace('.', '_')))


@pytest.mark.experiments_mark
class TestExperimentEphemeralTokenViewV1(BaseViewTest):
    HAS_AUTH = False
    factory_class = ExperimentFactory

    def setUp(self):
        super().setUp()
        self.auth_user = self.auth_client.user
        self.project = ProjectFactory(user=self.auth_client.user)
        self.experiment = self.factory_class(project=self.project)
        self.other_experiment = self.factory_class(project=self.project)
        self.url = '/{}/{}/{}/experiments/{}/ephemeraltoken'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.experiment.id)
        self.other_url = '/{}/{}/{}/experiments/{}/ephemeraltoken'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.other_experiment.id)

    @staticmethod
    def create_ephemeral_token(experiment, **kwargs):
        scope = RedisEphemeralTokens.get_scope(user=experiment.user.id,
                                               model='experiment',
                                               object_id=experiment.id)
        return RedisEphemeralTokens.generate(scope=scope, **kwargs)

    def test_is_forbidden_for_non_running_or_scheduled_experiment(self):
        ephemeral_token = self.create_ephemeral_token(self.experiment)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_client = EphemeralClient(token=token)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        self.assertEqual(ephemeral_token.get_state(), None)

    def test_using_other_experiment_token(self):
        ephemeral_token = self.create_ephemeral_token(self.other_experiment)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_client = EphemeralClient(token=token)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        self.assertEqual(ephemeral_token.get_state(), None)

    def test_using_timed_out_experiment_token(self):
        self.experiment.set_status(status=JobLifeCycle.RUNNING)
        ephemeral_token = self.create_ephemeral_token(self.experiment, ttl=1)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_client = EphemeralClient(token=token)
        time.sleep(1.1)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        self.assertEqual(ephemeral_token.get_state(), None)

    def test_using_used_experiment_token(self):
        self.experiment.set_status(status=JobLifeCycle.RUNNING)
        ephemeral_token = self.create_ephemeral_token(self.experiment)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_token.clear()
        ephemeral_client = EphemeralClient(token=token)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        self.assertEqual(ephemeral_token.get_state(), None)

    def test_using_scheduled_experiment_token(self):
        self.experiment.set_status(status=ExperimentLifeCycle.SCHEDULED)
        ephemeral_token = self.create_ephemeral_token(self.experiment)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_client = EphemeralClient(token=token)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == {'token': self.experiment.user.tokens.last().key}
        self.assertEqual(ephemeral_token.get_state(), None)

    def test_using_starting_experiment_token(self):
        self.experiment.set_status(status=ExperimentLifeCycle.STARTING)
        ephemeral_token = self.create_ephemeral_token(self.experiment)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_client = EphemeralClient(token=token)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == {'token': self.experiment.user.tokens.last().key}
        self.assertEqual(ephemeral_token.get_state(), None)

    def test_using_running_experiment_token(self):
        self.experiment.set_status(status=ExperimentLifeCycle.RUNNING)
        ephemeral_token = self.create_ephemeral_token(self.experiment)
        token = RedisEphemeralTokens.create_header_token(ephemeral_token)
        ephemeral_client = EphemeralClient(token=token)
        resp = ephemeral_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == {'token': self.experiment.user.tokens.last().key}
        self.assertEqual(ephemeral_token.get_state(), None)


@pytest.mark.experiments_mark
class TestExperimentChartViewListViewV1(BaseViewTest):
    serializer_class = ExperimentChartViewSerializer
    model_class = ExperimentChartView
    factory_class = ExperimentChartViewFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/chartviews/'.format(API_V1,
                                                                 project.user.username,
                                                                 project.name,
                                                                 self.experiment.id)
        self.objects = [self.factory_class(experiment=self.experiment, name='view{}'.format(i))
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('created_at')

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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'charts': [{'id': '1'}, {'id': '2'}]}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.charts == data['charts']


@pytest.mark.experiments_mark
class TestExperimentChartViewDetailViewV1(BaseViewTest):
    serializer_class = ExperimentChartViewSerializer
    model_class = ExperimentChartView
    factory_class = ExperimentChartViewFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=self.project)
        self.object = self.factory_class(experiment=self.experiment)
        self.url = '/{}/{}/{}/experiments/{}/chartviews/{}/'.format(
            API_V1,
            self.experiment.project.user.username,
            self.experiment.project.name,
            self.experiment.id,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'charts': [{'uuid': 'id22'}, {'uuid': 'id23'}, {'uuid': 'id24'}, {'uuid': 'id25'}]}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['charts'] == data['charts']

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0


@pytest.mark.experiments_mark
class TestExperimentHeartBeatViewV1(BaseViewTest):
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/_heartbeat'.format(
            API_V1,
            project.user.username,
            project.name,
            self.experiment.id)

    def test_post_experiment_heartbeat(self):
        self.assertEqual(RedisHeartBeat.experiment_is_alive(self.experiment.id), False)
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(RedisHeartBeat.experiment_is_alive(self.experiment.id), True)

    def test_post_internal_experiment_heartbeat(self):
        self.assertEqual(RedisHeartBeat.experiment_is_alive(self.experiment.id), False)
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(RedisHeartBeat.experiment_is_alive(self.experiment.id), True)
