# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from polyaxon_client import settings
from polyaxon_client.tracking.base import BaseTracker
from polyaxon_client.tracking.in_cluster import ensure_in_custer


class Job(BaseTracker):
    def __init__(self,
                 project=None,
                 job_id=None,
                 client=None,
                 track_logs=True,
                 track_code=True,
                 track_env=True,
                 outputs_store=None):
        if project is None and settings.IN_CLUSTER:
            job_info = self.get_job_info()
            project = job_info['project_name']
            job_id = job_info['job_name'].split('.')[-1]
        super(Job, self).__init__(project=project,
                                  client=client,
                                  track_logs=track_logs,
                                  track_code=track_code,
                                  track_env=track_env,
                                  outputs_store=outputs_store)
        self.job_id = job_id
        self.job = None
        self.last_status = None

    @staticmethod
    def get_job_info():
        """Returns information about the job:
            * project_name
            * job_name
            * project_uuid
            * job_uuid
            * role
            * type
            * app
        """
        ensure_in_custer()

        info = os.getenv('POLYAXON_JOB_INFO', None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print('Could get experiment info, '
                  'please make sure this is running inside a polyaxon job.')
            return None
