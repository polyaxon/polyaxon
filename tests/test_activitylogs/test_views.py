import pytest

from rest_framework import status

import activitylogs
from api.activitylogs.serializers import ActivityLogsSerializer
from constants.urls import API_V1
from db.models.activitylogs import ActivityLog
from event_manager.events.experiment import EXPERIMENT_DELETED_TRIGGERED
from event_manager.events.job import JOB_VIEWED
from event_manager.events.project import PROJECT_DELETED_TRIGGERED
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseViewTest


@pytest.mark.bookmarks_mark
class TestActivityLogsListViewV1(BaseViewTest):
    HAS_AUTH = True
    DISABLE_RUNNER = True
    model_class = ActivityLog
    serializer_class = ActivityLogsSerializer
    num_objects = 3

    def set_objects(self):
        self.user = self.auth_client.user
        self.project = ProjectFactory()
        activitylogs.record(event_type=PROJECT_DELETED_TRIGGERED,
                            instance=self.project,
                            actor_id=self.user.id)
        self.experiment = ExperimentFactory()
        activitylogs.record(event_type=EXPERIMENT_DELETED_TRIGGERED,
                            instance=self.experiment,
                            actor_id=self.user.id)
        self.job = JobFactory()
        activitylogs.record(event_type=JOB_VIEWED,
                            instance=self.job,
                            actor_id=self.user.id)

    def set_url(self):
        self.url = '/{}/activitylogs/'.format(API_V1)

    def setUp(self):
        super().setUp()
        activitylogs.validate()
        activitylogs.setup()

        self.set_objects()
        self.set_url()

        self.objects = self.model_class.objects.all()
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('-created_at')

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


@pytest.mark.bookmarks_mark
class TestProjectActivityLogsListViewV1(TestActivityLogsListViewV1):
    def set_objects(self):
        self.user = self.auth_client.user
        self.project = ProjectFactory(user=self.user)
        activitylogs.record(event_type=PROJECT_DELETED_TRIGGERED,
                            instance=self.project,
                            actor_id=self.user.id)
        self.experiment = ExperimentFactory(project=self.project)
        activitylogs.record(event_type=EXPERIMENT_DELETED_TRIGGERED,
                            instance=self.experiment,
                            actor_id=self.user.id)
        self.job = JobFactory(project=self.project)
        activitylogs.record(event_type=JOB_VIEWED,
                            instance=self.job,
                            actor_id=self.user.id)

    def set_url(self):
        self.url = '/{}/activitylogs/{}'.format(API_V1, self.project.id)
