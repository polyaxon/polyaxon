import uuid

import pytest

from rest_framework import status

import activitylogs

from api.activitylogs.serializers import ActivityLogsSerializer
from constants.urls import API_V1
from db.models.activitylogs import ActivityLog
from event_manager.events.experiment import EXPERIMENT_DELETED_TRIGGERED, EXPERIMENT_VIEWED
from event_manager.events.job import JOB_CREATED, JOB_VIEWED
from event_manager.events.project import PROJECT_DELETED_TRIGGERED, PROJECT_VIEWED
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseViewTest


@pytest.mark.activitylogs_mark
class TestActivityLogsListViewV1(BaseViewTest):
    HAS_AUTH = True
    model_class = ActivityLog
    serializer_class = ActivityLogsSerializer
    num_objects = 3

    def set_objects(self):
        self.user = self.auth_client.user
        self.project = ProjectFactory()
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=PROJECT_DELETED_TRIGGERED,
                            instance=self.project,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        self.experiment = ExperimentFactory()
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=EXPERIMENT_DELETED_TRIGGERED,
                            instance=self.experiment,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        self.job = JobFactory()
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=JOB_CREATED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=JOB_VIEWED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)

    def set_url(self):
        self.url = '/{}/activitylogs/'.format(API_V1)

    def set_queryset(self):
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('-created_at')
        self.filtered_queryset = self.queryset.filter(
            event_type__in=activitylogs.default_manager.user_write_events()
        )

    def setUp(self):
        super().setUp()
        activitylogs.validate()
        activitylogs.setup()

        self.set_objects()
        self.set_url()
        self.set_queryset()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == self.filtered_queryset.count()

        data = resp.data['results']
        assert len(data) == self.queryset.count() - 1
        assert len(data) == self.filtered_queryset.count()
        assert data == self.serializer_class(self.filtered_queryset, many=True).data  # noqa

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count() - 1
        assert resp.data['count'] == self.filtered_queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.filtered_queryset[:limit], many=True).data  # noqa

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.filtered_queryset[limit:], many=True).data  # noqa


@pytest.mark.activitylogs_mark
class TestHistoryLogsListViewV1(TestActivityLogsListViewV1):
    def set_objects(self):
        self.user = self.auth_client.user
        self.project = ProjectFactory()
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=PROJECT_VIEWED,
                            instance=self.project,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        self.experiment = ExperimentFactory()
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=EXPERIMENT_VIEWED,
                            instance=self.experiment,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        self.job = JobFactory()
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=JOB_CREATED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=JOB_VIEWED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)

    def set_url(self):
        self.url = '/{}/historylogs/'.format(API_V1)

    def set_queryset(self):
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('-created_at')
        self.filtered_queryset = self.queryset.filter(
            event_type__in=activitylogs.default_manager.user_view_events()
        )


@pytest.mark.activitylogs_mark
class TestProjectActivityLogsListViewV1(TestActivityLogsListViewV1):
    def set_objects(self):
        self.user = self.auth_client.user
        self.project = ProjectFactory(user=self.user)
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=PROJECT_DELETED_TRIGGERED,
                            instance=self.project,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        self.experiment = ExperimentFactory(project=self.project)
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=EXPERIMENT_DELETED_TRIGGERED,
                            instance=self.experiment,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        self.job = JobFactory(project=self.project)
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=JOB_CREATED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=JOB_VIEWED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)

    def set_url(self):
        self.url = '/{}/activitylogs/{}/{}/'.format(API_V1,
                                                    self.project.user.username,
                                                    self.project.name)

    def test_get_non_existing_project(self):
        resp = self.auth_client.get('/{}/activitylogs/foo/bar/')
        assert resp.status_code == status.HTTP_404_NOT_FOUND
