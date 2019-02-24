from unittest.mock import patch

import pytest

from rest_framework import status

from api.experiment_groups import queries
from api.experiment_groups.serializers import (
    BookmarkedExperimentGroupSerializer,
    ExperimentGroupChartViewSerializer,
    ExperimentGroupDetailSerializer,
    ExperimentGroupStatusSerializer
)
from api.experiments.serializers import ExperimentMetricSerializer
from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.bookmarks import Bookmark
from db.models.build_jobs import BuildJobStatus
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupChartView,
    ExperimentGroupStatus
)
from db.models.experiments import Experiment, ExperimentMetric
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import (
    ExperimentGroupChartViewFactory,
    ExperimentGroupFactory,
    ExperimentGroupStatusFactory
)
from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentJobFactory,
    ExperimentMetricFactory,
    ExperimentStatusFactory
)
from factories.factory_projects import ProjectFactory
from factories.fixtures import experiment_group_spec_content_early_stopping
from tests.utils import BaseViewTest


@pytest.mark.experiment_groups_mark
class TestProjectExperimentGroupListViewV1(BaseViewTest):
    serializer_class = BookmarkedExperimentGroupSerializer
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

        self.objects = [self.factory_class(project=self.project)
                        for _ in range(self.num_objects)]
        self.queryset = queries.groups.filter(project=self.project)
        # Other objects
        self.other_object = self.factory_class(project=self.other_project)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.num_objects

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data['results']
        self.other_object.refresh_from_db()
        assert data[0] == self.serializer_class(self.other_object).data

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

        # Search concurrency
        resp = self.auth_client.get(self.url +
                                    '?query=concurrency:1')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        # Search concurrency
        resp = self.auth_client.get(self.url +
                                    '?query=concurrency:{}'.format(self.objects[0].concurrency))
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        # Search hp search algorithm
        resp = self.auth_client.get(self.url +
                                    '?query=search_algorithm:grid')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 3

        # Search hp search algorithm
        resp = self.auth_client.get(self.url +
                                    '?query=search_algorithm:random')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        # Search hp search algorithm
        resp = self.auth_client.get(self.url +
                                    '?query=search_algorithm:grid|random')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 3

        # Create a new object with random search
        self.factory_class(project=self.project,
                           content=experiment_group_spec_content_early_stopping)

        # Search hp search algorithm
        resp = self.auth_client.get(self.url +
                                    '?query=search_algorithm:random')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 1

        # Search hp search algorithm
        resp = self.auth_client.get(self.url +
                                    '?query=search_algorithm:grid|random')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects) + 1

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

hptuning:
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
        assert last_object.hptuning is not None
        assert last_object.hptuning['concurrency'] == 3
        assert last_object.hptuning['matrix']['lr'] is not None
        assert last_object.is_study is True

        # Creating a study with selection ignores selection
        experiments = [ExperimentFactory(project=self.project) for _ in range(2)]
        experiment_ids = [xp.id for xp in experiments]
        data = {'content': content, 'description': 'new-deep', 'experiment_ids': experiment_ids}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.is_study is True
        assert last_object.selection_experiments.count() == 0

    def test_create_without_content_passes_if_no_spec_validation_requested(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.content is None
        assert last_object.is_selection is True

        # Creating a selection with experiment ids
        experiments = [ExperimentFactory(project=self.project) for _ in range(2)]
        experiment_ids = [xp.id for xp in experiments]
        data = {'experiment_ids': experiment_ids}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.is_study is False
        assert last_object.selection_experiments.count() == 2

        # Creating a selection with an invalid experiment id raises
        experiments.append(ExperimentFactory())
        experiment_ids = [xp.id for xp in experiments]
        data = {'experiment_ids': experiment_ids}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.queryset.count() == self.num_objects + 2

    def test_create_with_hptuning(self):
        data = {
            'hptuning': {
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
        assert last_object.is_study is False


@pytest.mark.experiment_groups_mark
class TestExperimentGroupDetailViewV1(BaseViewTest):
    serializer_class = ExperimentGroupDetailSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/groups/{}/'.format(API_V1,
                                                 project.user.username,
                                                 project.name,
                                                 self.object.id)
        self.queryset = self.model_class.objects.all()

        # Add 2 experiments
        for _ in range(2):
            ExperimentFactory(experiment_group=self.object)

        self.object_query = queries.groups_details.get(id=self.object.id)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object_query).data
        assert resp.data['num_pending_experiments'] == 2

    def test_patch(self):
        new_description = 'updated_description'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description
        assert new_object.experiments.count() == 2

        data = {'name': 'new_name'}
        assert self.object.name is None
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']

    def test_delete_archives_deletes_immediately_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        assert Experiment.objects.count() == 2
        experiment = ExperimentFactory(project=self.object.project,
                                       experiment_group=self.object)
        # Set the object to running
        self.object.set_status(ExperimentGroupLifeCycle.RUNNING)
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_stop_experiments.apply_async') as scheduler_mock:
            resp = self.auth_client.delete(self.url)
        assert scheduler_mock.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Delete
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0
        assert Experiment.all.count() == 0
        assert Experiment.objects.count() == 0

    def test_delete_archives_and_schedules_deletion(self):
        assert self.model_class.objects.count() == 1
        experiment = ExperimentFactory(project=self.object.project,
                                       experiment_group=self.object)
        assert Experiment.objects.count() == 3
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_schedule_deletion.apply_async') as scheduler_mock:
            resp = self.auth_client.delete(self.url)
        assert scheduler_mock.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Patched
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        assert Experiment.all.count() == 3
        assert Experiment.objects.count() == 0

    def test_archive_schedule_deletion(self):
        assert self.model_class.objects.count() == 1
        experiment = ExperimentFactory(project=self.object.project,
                                       experiment_group=self.object)
        assert Experiment.objects.count() == 3
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1
        assert Experiment.all.count() == 3
        assert Experiment.objects.count() == 3

    def test_archive_schedule_archives_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        experiment = ExperimentFactory(project=self.object.project,
                                       experiment_group=self.object)
        assert Experiment.objects.count() == 3
        # Set the object to running
        self.object.set_status(ExperimentGroupLifeCycle.RUNNING)
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_stop_experiments.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        assert Experiment.all.count() == 3
        assert Experiment.objects.count() == 0

    def test_restore(self):
        ExperimentFactory(project=self.object.project, experiment_group=self.object)
        assert Experiment.objects.count() == 3
        self.object.archive()
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        assert Experiment.all.count() == 3
        assert Experiment.objects.count() == 0

        resp = self.auth_client.post(self.url + 'restore/')
        assert resp.status_code == status.HTTP_200_OK

        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1
        assert Experiment.all.count() == 3
        assert Experiment.objects.count() == 3


@pytest.mark.experiment_groups_mark
class TestExperimentGroupSelectionViewV1(BaseViewTest):
    serializer_class = ExperimentGroupDetailSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=self.project, content=None)
        self.url = '/{}/{}/{}/selections/{}/'.format(API_V1,
                                                     self.project.user.username,
                                                     self.project.name,
                                                     self.object.id)
        self.queryset = self.model_class.objects.all()
        self.object_query = queries.groups_details.get(id=self.object.id)
        assert self.object.is_selection

    def test_add_experiments(self):
        # Creating a selection with experiment ids
        experiments = [ExperimentFactory(project=self.project) for _ in range(2)]
        experiment_ids = [xp.id for xp in experiments]
        data = {'experiment_ids': experiment_ids}
        resp = self.auth_client.put(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.selection_experiments.count() == 2

        # Creating a selection with an invalid experiment id raises
        experiments.append(ExperimentFactory())
        experiment_ids = [xp.id for xp in experiments]
        data = {'experiment_ids': experiment_ids}
        resp = self.auth_client.put(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.object.selection_experiments.count() == 2

        # Manually setting selection
        self.object.selection_experiments.set([])
        assert self.object.selection_experiments.count() == 0
        self.object.selection_experiments.set([ExperimentFactory(project=self.project)])
        assert self.object.selection_experiments.count() == 1

        # Adding experiments
        experiments.pop()
        experiment_ids = [xp.id for xp in experiments]
        data = {'experiment_ids': experiment_ids, 'operation': 'add'}
        resp = self.auth_client.put(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.selection_experiments.count() == 3

        # Removing experiments
        data = {'experiment_ids': experiment_ids, 'operation': 'remove'}
        resp = self.auth_client.put(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.selection_experiments.count() == 1

        # Settings experiments
        data = {'experiment_ids': experiment_ids}
        resp = self.auth_client.put(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.selection_experiments.count() == 2

        # Using invalid operation
        data = {'experiment_ids': experiment_ids, 'operation': 'foo'}
        resp = self.auth_client.put(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.object.selection_experiments.count() == 2


@pytest.mark.experiment_groups_mark
class TestStopExperimentGroupViewV1(BaseViewTest):
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True
    DISABLE_EXECUTOR = False
    DISABLE_RUNNER = False

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        with patch('hpsearch.tasks.grid.hp_grid_search_start.apply_async') as mock_fct:
            with patch('scheduler.dockerizer_scheduler.create_build_job') as mock_start:
                build = BuildJobFactory()
                BuildJobStatus.objects.create(status=JobLifeCycle.SUCCEEDED, job=build)
                mock_start.return_value = build, True, True
                self.object = self.factory_class(project=project)

        assert mock_fct.call_count == 2
        # Add a running experiment
        experiment = ExperimentFactory(experiment_group=self.object)
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        self.url = '/{}/{}/{}/groups/{}/stop'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)

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
        with patch('scheduler.experiment_scheduler.stop_experiment') as stop_mock_fct:  # noqa
            with patch('logs_handlers.collectors.'
                       'logs_collect_experiment_jobs') as logs_collector_mock_fct:
                resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_200_OK
        assert self.object.stopped_experiments.count() == 3
        # 3 and only 1 running the other will have a stopped directly
        assert stop_mock_fct.call_count == 1
        assert logs_collector_mock_fct.call_count == 1

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


@pytest.mark.experiment_groups_mark
class TestExperimentGroupStatusListViewV1(BaseViewTest):
    serializer_class = ExperimentGroupStatusSerializer
    model_class = ExperimentGroupStatus
    factory_class = ExperimentGroupStatusFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        with patch.object(ExperimentGroup, 'set_status') as _:  # noqa
            self.experiment_group = ExperimentGroupFactory(project=project)
        self.url = '/{}/{}/{}/groups/{}/statuses/'.format(API_V1,
                                                          project.user.username,
                                                          project.name,
                                                          self.experiment_group.id)
        self.objects = [self.factory_class(experiment_group=self.experiment_group,
                                           status=ExperimentGroupLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter(experiment_group=self.experiment_group)
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
        assert last_object.status == ExperimentGroupLifeCycle.CREATED

        data = {'status': ExperimentGroupLifeCycle.RUNNING}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.experiment_group == self.experiment_group
        assert last_object.status == data['status']


@pytest.mark.experiment_groups_mark
class TestExperimentGroupChartViewListViewV1(BaseViewTest):
    serializer_class = ExperimentGroupChartViewSerializer
    model_class = ExperimentGroupChartView
    factory_class = ExperimentGroupChartViewFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.group = ExperimentGroupFactory(project=project)
        self.url = '/{}/{}/{}/groups/{}/chartviews/'.format(API_V1,
                                                            project.user.username,
                                                            project.name,
                                                            self.group.id)
        self.objects = [self.factory_class(experiment_group=self.group, name='view{}'.format(i))
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
        assert last_object.experiment_group == self.group
        assert last_object.charts == data['charts']


@pytest.mark.experiment_groups_mark
class TestExperimentGroupChartViewDetailViewV1(BaseViewTest):
    serializer_class = ExperimentGroupChartViewSerializer
    model_class = ExperimentGroupChartView
    factory_class = ExperimentGroupChartViewFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.group = ExperimentGroupFactory(project=self.project)
        self.object = self.factory_class(experiment_group=self.group)
        self.url = '/{}/{}/{}/groups/{}/chartviews/{}/'.format(
            API_V1,
            self.group.project.user.username,
            self.group.project.name,
            self.group.id,
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


@pytest.mark.experiment_groups_mark
class TestExperimentGroupMetricListViewV1(BaseViewTest):
    serializer_class = ExperimentMetricSerializer
    model_class = ExperimentMetric
    factory_class = ExperimentMetricFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.group = ExperimentGroupFactory(project=project)
        self.selection = ExperimentGroupFactory(project=project, content=None)
        self.experiment1 = ExperimentFactory(project=project, experiment_group=self.group)
        self.experiment2 = ExperimentFactory(project=project, experiment_group=self.group)
        self.experiment3 = ExperimentFactory(project=project)
        self.selection.selection_experiments.set([self.experiment3])
        self.group_url = '/{}/{}/{}/groups/{}/metrics/'.format(API_V1,
                                                               project.user.username,
                                                               project.name,
                                                               self.group.id)
        self.url = self.group_url
        self.selection_url = '/{}/{}/{}/groups/{}/metrics/'.format(API_V1,
                                                                   project.user.username,
                                                                   project.name,
                                                                   self.selection.id)
        self.objects1 = [
            self.factory_class(experiment=self.experiment1, values={'accuracy': i / 10})
            for i in range(self.num_objects)]
        self.objects2 = [
            self.factory_class(experiment=self.experiment2, values={'accuracy': i / 10})
            for i in range(self.num_objects)]
        self.objects3 = [
            self.factory_class(experiment=self.experiment3, values={'accuracy': i / 10})
            for i in range(self.num_objects)]

        # Add a random experiment and metric
        self.experiment4 = ExperimentFactory(project=project)
        self.factory_class(experiment=self.experiment4, values={'accuracy': 0.9})

        self.group_queryset = self.model_class.objects.filter(
            experiment__experiment_group=self.group)
        self.group_queryset = self.group_queryset.order_by('created_at')

        self.selection_queryset = self.model_class.objects.filter(
            experiment__selections=self.selection)
        self.selection_queryset = self.selection_queryset.order_by('created_at')

    def test_get(self):
        resp = self.auth_client.get(self.group_url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 2 * self.num_objects

        data = resp.data['results']
        assert len(data) == self.group_queryset.count()
        assert data == self.serializer_class(self.group_queryset, many=True).data

        resp = self.auth_client.get(self.selection_url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.num_objects

        data = resp.data['results']
        assert len(data) == self.selection_queryset.count()
        assert data == self.serializer_class(self.selection_queryset, many=True).data

    def test_pagination(self):
        limit = (self.num_objects * 2) - 1
        resp = self.auth_client.get("{}?limit={}".format(self.group_url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.group_queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.group_queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.group_queryset[limit:], many=True).data
