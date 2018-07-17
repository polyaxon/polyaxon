# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.job import JobConfig, JobStatusConfig


class JobClient(PolyaxonClient):
    """Client to get jobs from the server"""
    ENDPOINT = "/"

    def get_job(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id)
        try:
            response = self.get(request_url)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job.')
            return None

    def update_job(self, username, project_name, job_id, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id)
        try:
            response = self.patch(request_url, json_data=patch_dict)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating job.')
            return None

    def delete_job(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id)
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting job.')
            return None

    def get_statuses(self, username, project_name, job_id, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'statuses')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job statuses.')
            return None

    def restart(self, username, project_name, job_id, config=None, update_code=None):
        """Restart an job."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'restart')

        data = {}
        if config:
            data['config'] = config
        if update_code:
            data['update_code'] = update_code

        try:
            response = self.post(request_url, json_data=data)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while restarting the job.')
            return None

    def resume(self, username, project_name, job_id, config=None, update_code=None):
        """Resume a job."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'resume')

        data = {}
        if config:
            data['config'] = config
        if update_code:
            data['update_code'] = update_code

        try:
            response = self.post(request_url, json_data=data)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while resuming the job.')
            return None

    def copy(self, username, project_name, job_id, config=None, update_code=None):
        """Copy an job."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'copy')

        data = {}
        if config:
            data['config'] = config
        if update_code:
            data['update_code'] = update_code

        try:
            response = self.post(request_url, json_data=data)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while copying the job.')
            return None

    def stop(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping job.')
            return None

    def bookmark(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'bookmark')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while bookmarking job.')
            return None

    def unbookmark(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'unbookmark')
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while unbookmarking job.')
            return None

    def resources(self, username, project_name, job_id, message_handler=None):
        """Streams jobs resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'resources')
        self.socket(request_url, message_handler=message_handler)

    # pylint:disable=inconsistent-return-statements
    def logs(self, username, project_name, job_id, stream=True, message_handler=None):
        """Streams jobs logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        if not stream:
            request_url = self._build_url(self._get_http_url(),
                                          username,
                                          project_name,
                                          'jobs',
                                          job_id,
                                          'logs')

            try:
                return self.get(request_url)
            except PolyaxonException as e:
                self.handle_exception(e=e, log_message='Error while retrieving jobs.')
                return []

        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'logs')
        self.socket(request_url, message_handler=message_handler)

    def download_outputs(self, username, project_name, job_id):
        """Downloads outputs for this job to the current dir."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'jobs',
                                      job_id,
                                      'outputs')

        try:
            response = self.download(
                request_url,
                '{}.{}.{}.tar.gz'.format(username, project_name, job_id))
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while downloading job outputs.')
            return None
