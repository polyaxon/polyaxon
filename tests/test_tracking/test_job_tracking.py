# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from tests.utils import TestEnvVarsCase

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking.job import Job


class TestJobTracking(TestEnvVarsCase):
    def setUp(self):
        super(TestJobTracking, self).setUp()
        settings.IS_MANAGED = True

    def test_job_info_checks_is_managed(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            Job.get_job_info()

    def test_empty_job_info(self):
        self.check_empty_value('POLYAXON_JOB_INFO', Job.get_job_info)

    def test_non_dict_job_info(self):
        self.check_non_dict_value('POLYAXON_JOB_INFO', Job.get_job_info)

    def test_dict_job_info(self):
        job_info = {
            "project_name": "project_bar",
            "job_name": "project_bar.jobs.1",
            "project_uuid": uuid.uuid4().hex,
            "job_uuid": uuid.uuid4().hex,
        }
        self.check_valid_dict_value('POLYAXON_JOB_INFO',
                                    Job.get_job_info,
                                    job_info)
