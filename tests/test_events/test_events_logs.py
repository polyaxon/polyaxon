# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import uuid
import os

from unittest.mock import patch

from polyaxon_schemas.utils import TaskType

from events.tasks import handle_events_job_logs
from experiments.utils import get_experiment_logs_path
from factories.factory_experiments import ExperimentFactory

from tests.utils import BaseTest


class TestEventsLogsHandling(BaseTest):
    @staticmethod
    def file_line_count(filename):
        return len([_ for _ in open(filename)])

    def test_handle_events_job_logs_create_one_handler(self):
        with patch('experiments.tasks.build_experiment.apply_async') as mock_fct:
            experiment = ExperimentFactory()

        params = dict(experiment_name=experiment.unique_name,
                      experiment_uuid=experiment.uuid.hex,
                      job_uuid=uuid.uuid4().hex,
                      log_line='First test',
                      persist=True,
                      task_type=TaskType.MASTER,
                      task_idx=0)
        handle_events_job_logs(**params)

        # Check new log path is created
        log_path = get_experiment_logs_path(experiment.unique_name)
        assert os.path.exists(log_path) is True

        # Check the logger has no file handler, and one line created
        xp_logger = logging.getLogger(experiment.unique_name)
        assert len(xp_logger.handlers) == 0
        assert self.file_line_count(log_path) == 1

        # Calling again the task should not reuse handler, and create a new line
        handle_events_job_logs(**params)

        # Check the logger has no file handler, and one line created
        xp_logger = logging.getLogger(experiment.unique_name)
        assert len(xp_logger.handlers) == 0
        assert self.file_line_count(log_path) == 2
