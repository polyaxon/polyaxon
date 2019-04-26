# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.handlers.conf import setup_logging
from polyaxon_client.tracking.base import BaseTracker
from polyaxon_client.tracking.is_managed import ensure_is_managed
from polyaxon_client.tracking.no_op import check_no_op
from polyaxon_client.tracking.paths import (
    get_base_outputs_path,
    get_data_paths,
    get_log_level,
    get_outputs_path,
    get_outputs_refs_paths
)
from polyaxon_client.tracking.utils.backend import OTHER_BACKEND
from polyaxon_client.tracking.utils.code_reference import get_code_reference
from polyaxon_client.tracking.utils.env import get_run_env


class BaseJob(BaseTracker):
    @check_no_op
    def __init__(self,
                 project=None,
                 job_id=None,
                 job_type=None,
                 client=None,
                 track_logs=True,
                 track_code=True,
                 track_env=True,
                 outputs_store=None):
        if project is None and settings.IS_MANAGED and not self.is_notebook_job:
            job_info = self.get_job_info()
            project = job_info['project_name']
            job_id = job_info['job_name'].split('.')[-1]
            job_type = job_info['job_name'].split('.')[-2]

        super(BaseJob, self).__init__(project=project,
                                      client=client,
                                      track_logs=track_logs,
                                      track_code=track_code,
                                      track_env=track_env,
                                      outputs_store=outputs_store)
        self.job_id = job_id
        self.job_type = job_type
        self.job = None
        self.last_status = None

    @check_no_op
    def get_entity_data(self):
        if self.job_type == 'jobs':
            self._entity_data = self.client_backend.get_job(
                username=self.username,
                project_name=self.project_name,
                job_id=self.job_id)
            return
        elif self.job_type == 'builds':
            self._entity_data = self.client_backend.get_build(
                username=self.username,
                project_name=self.project_name,
                job_id=self.job_id)
            return
        raise PolyaxonClientException('Job type {} not supported'.format(self.job_type))

    @property
    def client_backend(self):
        if settings.NO_OP:
            return None

        if self.job_type == 'jobs':
            return self.client.job
        elif self.job_type == 'builds':
            return self.client.build_job
        raise PolyaxonClientException('Job type {} not supported'.format(self.job_type))

    @check_no_op
    def _set_health_url(self):
        health_url = self.client_backend.get_heartbeat_url(
            username=self.username,
            project_name=self.project_name,
            job_id=self.job_id)
        self.client.set_health_check(url=health_url)
        self._health_is_running = True

    @check_no_op
    def _unset_health_url(self):
        health_url = self.client_backend.get_heartbeat_url(
            username=self.username,
            project_name=self.project_name,
            job_id=self.job_id)
        self.client.unset_health_check(url=health_url)
        self._health_is_running = False

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
        if settings.NO_OP:
            return None

        ensure_is_managed()

        info = os.getenv('POLYAXON_JOB_INFO', None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print('Could get experiment info, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @check_no_op
    def log_status(self, status, message=None, traceback=None):
        self.client_backend.create_status(username=self.username,
                                          project_name=self.project_name,
                                          job_id=self.job_id,
                                          status=status,
                                          message=message,
                                          traceback=traceback,
                                          background=True)

    @check_no_op
    def send_logs(self, log_line):
        self.client_backend.send_logs(username=self.username,
                                      project_name=self.project_name,
                                      job_id=self.job_id,
                                      log_lines=log_line,
                                      periodic=True)

    @check_no_op
    def log_code_ref(self):
        self.client_backend.create_code_reference(username=self.username,
                                                  project_name=self.project_name,
                                                  job_id=self.job_id,
                                                  coderef=get_code_reference(),
                                                  background=True)


class Job(BaseJob):
    @check_no_op
    def __init__(self,
                 project=None,
                 job_id=None,
                 client=None,
                 track_logs=True,
                 track_code=True,
                 track_env=True,
                 outputs_store=None):
        super(Job, self).__init__(project=project,
                                  job_id=job_id,
                                  job_type='jobs',
                                  client=client,
                                  track_logs=track_logs,
                                  track_code=track_code,
                                  track_env=track_env,
                                  outputs_store=outputs_store)

    @check_no_op
    def create(self,
               name=None,
               backend=None,
               tags=None,
               description=None,
               content=None,
               build_id=None,
               base_outputs_path=None):
        job_config = {'run_env': get_run_env()} if self.track_env else {}
        if name:
            job_config['name'] = name
        if tags:
            job_config['tags'] = tags
        job_config['backend'] = OTHER_BACKEND
        if backend:
            job_config['backend'] = backend
        if description:
            job_config['description'] = description
        if content:
            job_config['content'] = self.client.project.validate_content(content=content)
        if build_id:
            job_config['build_job'] = str(build_id)
        job_config['is_managed'] = settings.IS_MANAGED

        job = self.client.project.create_job(
            username=self.username,
            project_name=self.project_name,
            job_config=job_config,
        )
        if not job:
            raise PolyaxonClientException('Could not create job.')
        if not settings.IS_MANAGED and self.track_logs:
            setup_logging(send_logs=self.send_logs)
        self.job_id = self._get_entity_id(job)
        self.job = job
        self.last_status = 'created'

        # Setup the outputs store
        base_outputs_path = base_outputs_path or get_base_outputs_path()
        if self.outputs_store is None and base_outputs_path:
            outputs_path = '{}/{}/{}/jobs/{}'.format(
                base_outputs_path, self.username, self.project_name, self.job_id)
            self.set_outputs_store(outputs_path=outputs_path)

        if self.track_code:
            self.log_code_ref()

        if not settings.IS_MANAGED:
            self._start()
            self._set_health_url()

        return self

    def _update(self, patch_dict):
        self.client.job.update_job(username=self.username,
                                   project_name=self.project_name,
                                   job_id=self.job_id,
                                   patch_dict=patch_dict,
                                   background=True)

    @check_no_op
    def log_artifact(self, file_path):
        self.job.outputs_store.upload_file(file_path)

    @check_no_op
    def log_artifacts(self, dir_path):
        self.job.outputs_store.upload_file(dir_path)

    @check_no_op
    def get_outputs_path(self):
        return get_outputs_path()

    @check_no_op
    def get_log_level(self):
        return get_log_level()

    @staticmethod
    def get_data_paths():
        if settings.NO_OP:
            return None
        return get_data_paths()

    @staticmethod
    def get_outputs_refs_paths():
        if settings.NO_OP:
            return None

        return get_outputs_refs_paths()
