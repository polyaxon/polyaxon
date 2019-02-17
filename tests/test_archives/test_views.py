import pytest

from rest_framework import status

from api.archives.serializers import (
    ArchivedBuildJobSerializer,
    ArchivedExperimentGroupSerializer,
    ArchivedExperimentSerializer,
    ArchivedJobSerializer,
    ArchivedProjectSerializer
)
from constants.urls import API_V1
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.projects import Project
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseViewTest


@pytest.mark.archives_mark
class BaseTestArchiveListViewV1(BaseViewTest):
    HAS_AUTH = True
    model_class = None
    serializer_class = None
    factory_class = None
    entity = ''
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.user = self.auth_client.user
        self.url = '/{}/archives/{}/{}'.format(API_V1, self.user.username, self.entity)
        self.objects = []
        for _ in range(self.num_objects):
            obj = self.factory_class(user=self.user)  # pylint:disable=not-callable
            obj.archive()
            self.objects.append(obj)

        # Other non archived objects
        self.other_object = self.factory_class(user=self.user)  # pylint:disable=not-callable

        self.queryset = self.model_class.archived.filter(user=self.user)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data  # noqa

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data  # noqa

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data  # noqa


@pytest.mark.archives_mark
class TestBuildArchiveListView(BaseTestArchiveListViewV1):
    HAS_AUTH = True
    model_class = BuildJob
    serializer_class = ArchivedBuildJobSerializer
    factory_class = BuildJobFactory
    entity = 'builds'


@pytest.mark.archives_mark
class TestJobArchiveListView(BaseTestArchiveListViewV1):
    HAS_AUTH = True
    model_class = Job
    serializer_class = ArchivedJobSerializer
    factory_class = JobFactory
    entity = 'jobs'


@pytest.mark.archives_mark
class TestExperimentArchiveListView(BaseTestArchiveListViewV1):
    HAS_AUTH = True
    model_class = Experiment
    serializer_class = ArchivedExperimentSerializer
    factory_class = ExperimentFactory
    entity = 'experiments'


@pytest.mark.archives_mark
class TestExperimentGroupArchiveListView(BaseTestArchiveListViewV1):
    HAS_AUTH = True
    model_class = ExperimentGroup
    serializer_class = ArchivedExperimentGroupSerializer
    factory_class = ExperimentGroupFactory
    entity = 'groups'


@pytest.mark.archives_mark
class TestProjectArchiveListView(BaseTestArchiveListViewV1):
    HAS_AUTH = True
    model_class = Project
    serializer_class = ArchivedProjectSerializer
    factory_class = ProjectFactory
    entity = 'projects'


del BaseTestArchiveListViewV1
