import uuid

import pytest

import activitylogs

from api.activitylogs.serializers import ActivityLogsSerializer
from db.models.activitylogs import ActivityLog
from event_manager import event_context
from event_manager.events.experiment import EXPERIMENT_DELETED_TRIGGERED
from event_manager.events.job import JOB_VIEWED
from event_manager.events.project import PROJECT_DELETED_TRIGGERED
from event_manager.events.user import USER_ACTIVATED
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from tests.utils import BaseTest


@pytest.mark.activitylogs_mark
class TestActivityLogsSerializer(BaseTest):
    serializer_class = ActivityLogsSerializer
    expected_keys = {
        'id',
        'event_action',
        'event_subject',
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
        activitylogs.record(ref_id=uuid.uuid4(),
                            event_type=USER_ACTIVATED,
                            instance=self.user,
                            actor_id=self.user.id,
                            actor_name=self.user.username)
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
                            event_type=JOB_VIEWED,
                            instance=self.job,
                            actor_id=self.user.id,
                            actor_name=self.user.username)

    def test_serialize_one_with_name(self):
        obj = ActivityLog.objects.first()
        data = self.serializer_class(obj).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('object_name') == obj.content_object.username
        assert data.pop('actor') == obj.actor.username
        assert data.pop('event_action') == event_context.get_event_action(obj.event_type)
        assert data.pop('event_subject') == event_context.get_event_subject(obj.event_type)
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(obj, k) == v

    def test_serialize_one_with_unique_name(self):
        obj = ActivityLog.objects.last()
        data = self.serializer_class(obj).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('object_name') == obj.content_object.unique_name
        assert data.pop('actor') == obj.actor.username
        assert data.pop('event_action') == event_context.get_event_action(obj.event_type)
        assert data.pop('event_subject') == event_context.get_event_subject(obj.event_type)
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(obj, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(ActivityLog.objects.all(), many=True).data
        assert len(data) == 4
        for d in data:
            assert set(d.keys()) == self.expected_keys
