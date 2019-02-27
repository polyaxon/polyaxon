# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.schemas import ExperimentJobConfig, ExperimentJobStatusConfig


class ExperimentJobApi(BaseApiHandler):
    """
    Api handler to get jobs from the server.
    """
    ENDPOINT = "/"

    def get_job(self, username, project_name, experiment_id, job_id):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'jobs',
                                     job_id)
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response_json=response.json(), config=ExperimentJobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving job')
            return None

    def get_statuses(self, username, project_name, experiment_id, job_id, page=1):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'jobs',
                                     job_id,
                                     'statuses')

        try:
            response = self.transport.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentJobStatusConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving job statuses')
            return []

    def resources(self, username, project_name, experiment_id, job_id,
                  message_handler=None):
        """Streams job resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self.build_url(self._get_ws_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'jobs',
                                     job_id,
                                     'resources')
        self.transport.stream(request_url, message_handler=message_handler)

    # pylint:disable=inconsistent-return-statements
    def logs(self,
             username,
             project_name,
             experiment_id,
             job_id,
             stream=True,
             message_handler=None):
        """Streams job logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        if not stream:
            request_url = self.build_url(self._get_http_url(),
                                         username,
                                         project_name,
                                         'experiments',
                                         experiment_id,
                                         'jobs',
                                         job_id,
                                         'logs')

            try:
                return self.transport.get(request_url)
            except PolyaxonClientException as e:
                self.transport.handle_exception(
                    e=e, log_message='Error while retrieving experiment job logs.')
                return []

        request_url = self.build_url(self._get_ws_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'jobs',
                                     job_id,
                                     'logs')
        self.transport.stream(request_url, message_handler=message_handler)
