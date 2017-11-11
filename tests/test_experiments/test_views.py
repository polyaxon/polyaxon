# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status

from polyaxon_k8s.constants import JobLifeCycle

from api.urls import API_V1
from clusters.constants import ExperimentLifeCycle
from experiments.models import (
    Experiment,
    ExperimentStatus,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentJobMessage,
)
from experiments.serializers import (
    ExperimentSerializer,
    ExperimentDetailSerializer,
    ExperimentStatusSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
)
from tests.factories.factory_experiments import (
    ExperimentFactory,
    ExperimentStatusFactory,
    ExperimentJobFactory,
    ExperimentJobStatusFactory,
)
from tests.factories.factory_projects import ProjectFactory, PolyaxonSpecFactory
from tests.utils import BaseTest


class TestProjectExperimentListViewV1(BaseTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.url = '/{}/projects/{}/experiments/'.format(API_V1, self.project.uuid.hex)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(project=self.project)

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


class TestPolyaxonSpecExperimentListViewV1(BaseTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.spec = PolyaxonSpecFactory()
        self.url = '/{}/specs/{}/experiments/'.format(API_V1, self.spec.uuid.hex)
        self.objects = [self.factory_class(spec=self.spec)
                        for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(spec=self.spec)

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


class TestExperimentListViewV1(BaseTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.url = '/{}/experiments/'.format(API_V1)
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

        object1 = self.objects[0]
        data = {'project': object1.project.id,
                'cluster': object1.cluster.id,
                'config': {'run': 'something'}}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1


class TestExperimentDetailViewV1(BaseTest):
    serializer_class = ExperimentDetailSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.object = self.factory_class()
        self.url = '/{}/experiments/{}/'.format(API_V1, self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            ExperimentJobFactory(experiment=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['jobs']) == 2
        assert resp.data['jobs'] == ExperimentJobSerializer(self.object.jobs.all(), many=True).data

    def test_patch(self):
        new_name = 'updated_xp_name'
        data = {'name': new_name}
        assert self.object.name != data['name']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.name != self.object.name
        assert new_object.name == new_name
        assert new_object.jobs.count() == 2

        # Update original experiment
        assert new_object.is_clone is False
        new_experiment = ExperimentFactory()
        data = {'original_experiment': new_experiment.id}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.name == new_name
        assert new_object.jobs.count() == 2
        assert new_object.is_clone is True
        assert new_object.original_experiment == new_experiment

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert ExperimentJob.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0
        assert ExperimentJob.objects.count() == 0


class TestExperimentStatusListViewV1(BaseTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()
        self.url = '/{}/experiments/{}/status/'.format(API_V1, self.experiment.uuid.hex)
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

        data = {'status': ExperimentLifeCycle.FINISHED}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.experiment == self.experiment
        assert last_object.status == data['status']


class TestExperimentStatusDetailViewV1(BaseTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()
        self.object = self.factory_class(experiment=self.experiment)
        self.url = '/{}/experiments/{}/status/{}/'.format(API_V1,
                                                          self.experiment.uuid.hex,
                                                          self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'status': ExperimentLifeCycle.FINISHED}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.model_class.objects.count() == 1


class TestExperimentJobListViewV1(BaseTest):
    serializer_class = ExperimentJobSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()
        self.url = '/{}/experiments/{}/jobs/'.format(API_V1, self.experiment.uuid.hex)
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


class TestExperimentJobDetailViewV1(BaseTest):
    serializer_class = ExperimentJobSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()
        self.object = self.factory_class(experiment=self.experiment)
        self.url = '/{}/experiments/{}/jobs/{}/'.format(API_V1,
                                                        self.experiment.uuid.hex,
                                                        self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

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
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0


class TestExperimentJobStatusListViewV1(BaseTest):
    serializer_class = ExperimentJobStatusSerializer
    model_class = ExperimentJobStatus
    factory_class = ExperimentJobStatusFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.experiment_job = ExperimentJobFactory()
        self.url = '/{}/experiments/{}/jobs/{}/status/'.format(
            API_V1,
            self.experiment_job.experiment.uuid.hex,
            self.experiment_job.uuid.hex)
        self.objects = [self.factory_class(job=self.experiment_job,
                                           status=JobLifeCycle.CHOICES[i][0])
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
        assert last_object.status == JobLifeCycle.CREATED

        data = {'status': JobLifeCycle.FINISHED}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.job == self.experiment_job
        assert last_object.status == data['status']


class TestExperimentJobStatusDetailViewV1(BaseTest):
    serializer_class = ExperimentJobStatusSerializer
    model_class = ExperimentJobStatus
    factory_class = ExperimentJobStatusFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.experiment_job = ExperimentJobFactory()
        self.object = self.factory_class(job=self.experiment_job)
        self.url = '/{}/experiments/{}/jobs/{}/status/{}'.format(
            API_V1,
            self.experiment_job.experiment.uuid.hex,
            self.experiment_job.uuid.hex,
            self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'message': {'reason': 'some reason'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        assert self.object.message is None
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.message is not None
        assert new_object.message.reason == 'some reason'

        data = {'message': {'reason': 'new reason'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.message.reason == 'new reason'
        assert ExperimentJobMessage.objects.count() == 1

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.model_class.objects.count() == 1
