# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings

from events.tasks import handle_events_job_statues
from experiments.models import ExperimentJobStatus
from spawner.utils.constants import JobLifeCycle
from spawner.utils.jobs import get_job_state

from factories.factory_experiments import ExperimentJobFactory
from tests.fixtures import status_raw_event, status_raw_event_with_conditions
from tests.utils import BaseTest


class TestEventsHandling(BaseTest):
    def test_handle_events_job_statues_for_non_existing_job(self):
        assert ExperimentJobStatus.objects.count() == 0
        job_state = get_job_state(event_type=status_raw_event['type'],
                                  event=status_raw_event['object'],
                                  job_container_name=settings.JOB_CONTAINER_NAME,
                                  experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)
        handle_events_job_statues(job_state.to_dict())
        assert ExperimentJobStatus.objects.count() == 0

    def test_handle_events_job_statues_for_existing_job_with_unknown_conditions(self):
        assert ExperimentJobStatus.objects.count() == 0
        job_state = get_job_state(event_type=status_raw_event['type'],
                                  event=status_raw_event['object'],
                                  job_container_name=settings.JOB_CONTAINER_NAME,
                                  experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)
        job_uuid = job_state.details.labels.job_id
        job = ExperimentJobFactory(uuid=job_uuid)
        handle_events_job_statues(job_state.to_dict())
        assert ExperimentJobStatus.objects.count() == 2
        statuses = ExperimentJobStatus.objects.filter(job=job).values_list('status', flat=True)
        assert set(statuses) == {JobLifeCycle.CREATED, JobLifeCycle.UNKNOWN}

    def test_handle_events_job_statues_for_existing_job_with_known_conditions(self):
        assert ExperimentJobStatus.objects.count() == 0
        job_state = get_job_state(event_type=status_raw_event_with_conditions['type'],
                                  event=status_raw_event_with_conditions['object'],
                                  job_container_name=settings.JOB_CONTAINER_NAME,
                                  experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)
        job_uuid = job_state.details.labels.job_id
        job = ExperimentJobFactory(uuid=job_uuid)
        handle_events_job_statues(job_state.to_dict())
        assert ExperimentJobStatus.objects.count() == 2
        statuses = ExperimentJobStatus.objects.filter(job=job).values_list('status', flat=True)
        assert set(statuses) == {JobLifeCycle.CREATED, JobLifeCycle.FAILED}
