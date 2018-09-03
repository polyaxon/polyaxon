# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import os

from polyaxon_client.tracking.base import ensure_in_custer


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
