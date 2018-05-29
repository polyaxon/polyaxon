# pylint:disable=too-many-lines
import pytest
from faker import Faker
from unittest.mock import patch

from rest_framework import status

from api.experiments.serializers import (
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
    ExperimentMetricSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.experiments import (
    Experiment,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,
    ExperimentStatus
)
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentJobFactory,
    ExperimentJobStatusFactory,
    ExperimentMetricFactory,
    ExperimentStatusFactory
)
from factories.factory_projects import ProjectFactory
from factories.fixtures import exec_experiment_spec_parsed_content
from libs.paths.experiments import get_experiment_logs_path
from polyaxon.urls import API_V1
from polyaxon_schemas.polyaxonfile.specification import ExperimentSpecification
from tests.utils import BaseViewTest


@pytest.mark.experiments_mark
class TestProjectExperimentListViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_RUNNER = True

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
        [self.factory_class(project=self.project, experiment_group=group) for _ in range(2)]
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

    def test_create_without_config_passes_if_no_spec_validation_requested(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.project == self.project
        assert last_object.config is None

    def test_create_with_declarations_and_dockerfile(self):
        data = {
            'declarations': {
                'lr': 0.1,
                'dropout': 0.5
            },
            'dockerfile': 'test'
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
        assert last_object.dockerfile == 'test'


@pytest.mark.experiments_mark
class TestExperimentGroupExperimentListViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory()
        self.objects = [self.factory_class(experiment_group=self.experiment_group)
                        for _ in range(self.num_objects)]
        self.url = '/{}/{}/{}/groups/{}/experiments/'.format(API_V1,
                                                             self.experiment_group.project.user,
                                                             self.experiment_group.project.name,
                                                             self.experiment_group.sequence)
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(experiment_group=self.experiment_group)

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


@pytest.mark.experiments_mark
class TestRunnerExperimentGroupExperimentListViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        content = """---
    version: 1

    kind: group

    settings:
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
        with patch('hpsearch.tasks.grid.hp_grid_search_start.retry') as start_fct:
            with patch('scheduler.tasks.experiments.'
                       'experiments_build.apply_async') as build_fct:
                self.experiment_group = ExperimentGroupFactory(content=content)

        assert start_fct.call_count == 1
        assert build_fct.call_count == 1
        assert self.experiment_group.specification.matrix_space == 3
        self.url = '/{}/{}/{}/groups/{}/experiments/'.format(API_V1,
                                                             self.experiment_group.project.user,
                                                             self.experiment_group.project.name,
                                                             self.experiment_group.sequence)
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(experiment_group=self.experiment_group)

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


@pytest.mark.experiments_mark
class TestExperimentListViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/experiments/'.format(API_V1,
                                                   self.project.user,
                                                   self.project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
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


@pytest.mark.experiments_mark
class TestExperimentDetailViewV1(BaseViewTest):
    serializer_class = ExperimentDetailSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/'.format(API_V1,
                                                      project.user.username,
                                                      project.name,
                                                      self.object.sequence)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for _ in range(2):
            ExperimentJobFactory(experiment=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data
        assert resp.data['num_jobs'] == 2

    def test_get_with_resource_reg_90(self):
        # Fix issue#90:
        # Failed to getting experiment when specify resources without framework in environment
        spec_content = """---
            version: 1

            kind: experiment

            environment:
              resources:
                gpu:
                  requests: 1
                  limits: 1
            run:
              image: my_image
              cmd: video_prediction_train --model=DNA --num_masks=1
        """
        spec_parsed_content = ExperimentSpecification.read(spec_content)

        project = ProjectFactory(user=self.auth_client.user)
        exp = self.factory_class(project=project, config=spec_parsed_content.parsed_data)
        url = '/{}/{}/{}/experiments/{}/'.format(API_V1,
                                                 project.user.username,
                                                 project.name,
                                                 exp.sequence)

        resp = self.auth_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        exp.refresh_from_db()
        assert resp.data == self.serializer_class(exp).data

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
        assert new_object.jobs.count() == 2

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

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        with patch('scheduler.experiment_scheduler.stop_experiment') as spawner_mock_stop:
            with patch('libs.paths.experiments.delete_path') as outputs_mock_stop:
                resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert outputs_mock_stop.call_count == 2  # Outputs and Logs
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
        assert ExperimentJob.objects.count() == 0


@pytest.mark.experiments_mark
class TestExperimentStatusListViewV1(BaseViewTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    num_objects = 3
    HAS_AUTH = True


    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
            with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/statuses/'.format(API_V1,
                                                               project.user.username,
                                                               project.name,
                                                               self.experiment.sequence)
        self.objects = [self.factory_class(experiment=self.experiment,
                                           status=ExperimentLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
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


@pytest.mark.experiments_mark
class TestExperimentMetricListViewV1(BaseViewTest):
    serializer_class = ExperimentMetricSerializer
    model_class = ExperimentMetric
    factory_class = ExperimentMetricFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:  # noqa
            with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/metrics/'.format(API_V1,
                                                              project.user.username,
                                                              project.name,
                                                              self.experiment.sequence)
        self.objects = [self.factory_class(experiment=self.experiment, values={'accuracy': i / 10})
                        for i in range(self.num_objects)]
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
            self.experiment.sequence,
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
            self.experiment.sequence)
        self.objects = [self.factory_class(experiment=self.experiment)
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
            self.experiment.sequence,
            self.object.sequence)
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
            experiment.sequence,
            self.experiment_job.sequence)
        self.objects = [self.factory_class(job=self.experiment_job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter(job=self.experiment_job)

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
            experiment.sequence,
            self.experiment_job.sequence,
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
class TestRestartExperimentViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/restart'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.sequence)
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
            self.object.sequence)
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

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/experiments/{}/copy'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.sequence)
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
            self.object.sequence)
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
class TestExperimentLogsViewV1(BaseViewTest):
    num_log_lines = 10
    HAS_AUTH = True
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/logs'.format(
            API_V1,
            project.user.username,
            project.name,
            experiment.sequence)

        log_path = get_experiment_logs_path(experiment.unique_name)
        fake = Faker()
        self.logs = []
        for _ in range(self.num_log_lines):
            self.logs.append(fake.sentence())
        with open(log_path, 'w') as file:
            for line in self.logs:
                file.write(line)
                file.write('\n')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs
