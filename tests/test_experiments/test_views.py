# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from rest_framework import status

from polyaxon.urls import API_V1
from experiments.models import (
    Experiment,
    ExperimentStatus,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,
)
from experiments.serializers import (
    ExperimentSerializer,
    ExperimentStatusSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
    ExperimentMetricSerializer,
)
from factories.fixtures import exec_experiment_spec_parsed_content
from spawner.utils.constants import JobLifeCycle, ExperimentLifeCycle

from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentStatusFactory,
    ExperimentJobFactory,
    ExperimentJobStatusFactory,
    ExperimentMetricFactory)
from factories.factory_projects import ProjectFactory, ExperimentGroupFactory
from tests.utils import BaseViewTest


class TestProjectExperimentListViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

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
        group = ExperimentGroupFactory(project=self.project)
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

        data = {'config': exec_experiment_spec_parsed_content.parsed_data}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


class TestExperimentGroupExperimentListViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        content = """---
    version: 1

    project:
      name: project1
      
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
        with patch('projects.tasks.start_group_experiments.retry') as _:
            self.experiment_group = ExperimentGroupFactory(content=content)
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


class TestExperimentDetailViewV1(BaseViewTest):
    serializer_class = ExperimentSerializer
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
        for i in range(2):
            ExperimentJobFactory(experiment=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert resp.data['num_jobs'] == 2

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
        with patch('spawner.scheduler.stop_experiment') as mock_stop:
            resp = self.auth_client.delete(self.url)
        assert mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
        assert ExperimentJob.objects.count() == 0


class TestExperimentStatusListViewV1(BaseViewTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
            with patch('experiments.tasks.start_experiment.delay') as _:
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


class TestExperimentMetricListViewV1(BaseViewTest):
    serializer_class = ExperimentMetricSerializer
    model_class = ExperimentMetric
    factory_class = ExperimentMetricFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
            with patch('experiments.tasks.start_experiment.delay') as _:
                project = ProjectFactory(user=self.auth_client.user)
                self.experiment = ExperimentFactory(project=project)
        self.url = '/{}/{}/{}/experiments/{}/metrics/'.format(API_V1,
                                                              project.user.username,
                                                              project.name,
                                                              self.experiment.sequence)
        self.objects = [self.factory_class(experiment=self.experiment, values = {'accuracy': i/10})
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

        data = {'values': {'precision': 0.9}}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.values == data['values']


class TestExperimentStatusDetailViewV1(BaseViewTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
            with patch('experiments.tasks.start_experiment.delay') as _:
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

        data = {'definition': {'key': 'my new kob k8s'}}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.definition == data['definition']


class TestExperimentJobDetailViewV1(BaseViewTest):
    serializer_class = ExperimentJobSerializer
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


class TestExperimentJobStatusListViewV1(BaseViewTest):
    serializer_class = ExperimentJobStatusSerializer
    model_class = ExperimentJobStatus
    factory_class = ExperimentJobStatusFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch('experiments.tasks.start_experiment.delay') as _:
            with patch.object(ExperimentJob, 'set_status') as _:
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


class TestExperimentJobStatusDetailViewV1(BaseViewTest):
    serializer_class = ExperimentJobStatusSerializer
    model_class = ExperimentJobStatus
    factory_class = ExperimentJobStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch('experiments.tasks.start_experiment.delay') as _:
            with patch.object(ExperimentJob, 'set_status') as _:
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
        with patch('experiments.tasks.start_experiment.delay') as _:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 2


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
        with patch('experiments.tasks.stop_experiment.delay') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1
