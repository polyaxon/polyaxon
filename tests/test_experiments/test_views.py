# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

from rest_framework import status

from api.urls import API_V1
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
    ExperimentJobMessageFactory,
)
from tests.utils import BaseTest


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

        # Create jobs for the experiment
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
