import logging
import os
import uuid

from unittest.mock import patch

import pytest

from events_handlers.tasks import handle_events_job_logs
from factories.factory_experiments import ExperimentFactory
from libs.paths.experiments import get_experiment_logs_path
from polyaxon_schemas.utils import TaskType
from tests.utils import BaseTest


@pytest.mark.monitors_mark
class TestEventsLogsHandling(BaseTest):
    @staticmethod
    def file_line_count(filename):
        return len([_ for _ in open(filename)])

    def test_handle_events_job_logs_create_one_handler(self):
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            experiment = ExperimentFactory()

        params = dict(experiment_name=experiment.unique_name,
                      experiment_uuid=experiment.uuid.hex,
                      job_uuid=uuid.uuid4().hex,
                      log_line='First test',
                      task_type=TaskType.MASTER,
                      task_idx=0)
        handle_events_job_logs(**params)

        # Check new log path is created
        log_path = get_experiment_logs_path(experiment.unique_name)
        assert os.path.exists(log_path) is True

        # Check the logger has no file handler, and one line created
        xp_logger = logging.getLogger(experiment.unique_name)
        assert len(xp_logger.handlers) == 0  # pylint:disable=len-as-condition
        assert self.file_line_count(log_path) == 1  # pylint:disable=len-as-condition

        # Calling again the task should not reuse handler, and create a new line
        handle_events_job_logs(**params)

        # Check the logger has no file handler, and one line created
        xp_logger = logging.getLogger(experiment.unique_name)
        assert len(xp_logger.handlers) == 0  # pylint:disable=len-as-condition
        assert self.file_line_count(log_path) == 2
