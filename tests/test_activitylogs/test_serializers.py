import pytest

import activitylogs
from api.activitylogs.serializers import ActivityLogsSerializer
from db.models.activitylogs import ActivityLog
from event_manager.events.experiment import EXPERIMENT_DELETED_TRIGGERED
from event_manager.events.job import JOB_VIEWED
from event_manager.events.project import PROJECT_DELETED_TRIGGERED
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from tests.utils import BaseTest


@pytest.mark.activitylogs_mark
class TestActivityLogsSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ActivityLogsSerializer
    expected_keys = {
        'event_type',
        'actor',
        'created_at',
        'object_id',
        'object_name'
    }

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        activitylogs.validate()
        activitylogs.setup()
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

    def test_serialize_one_with_name(self):
        obj = ActivityLog.objects.first()
        data = self.serializer_class(obj).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('object_name') == obj.content_object.unique_name
        assert data.pop('actor') == obj.actor.id
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(obj, k) == v

    def test_serialize_one_with_unique_name(self):
        obj = ActivityLog.objects.last()
        data = self.serializer_class(obj).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('object_name') == obj.content_object.unique_name
        assert data.pop('actor') == obj.actor.id
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(obj, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(ActivityLog.objects.all(), many=True).data
        assert len(data) == 3
        for d in data:
            assert set(d.keys()) == self.expected_keys

