# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import (
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentStatusConfig
)

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class ExperimentClient(PolyaxonClient):
    """Client to get experiments from the server"""
    ENDPOINT = "/experiments"

    def list_experiments(self, page=1):
        """This gets all experiments visible to the user from the server."""
        try:
            response = self.get(self._get_http_url(), params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def get_experiment(self, experiment_uuid):
        request_url = self._build_url(self._get_http_url(), experiment_uuid)
        try:
            response = self.get(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment')
            return None

    def update_experiment(self, experiment_uuid, patch_dict):
        request_url = self._build_url(self._get_http_url(), experiment_uuid)
        try:
            response = self.patch(request_url, json=patch_dict)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating experiment')
            return None

    def delete_experiment(self, experiment_uuid):
        request_url = self._build_url(self._get_http_url(), experiment_uuid)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment')
            return None

    def get_status(self, experiment_uuid):
        request_url = self._build_url(self._get_http_url(), experiment_uuid, 'statuses')
        try:
            response = self.get(request_url)
            return ExperimentStatusConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status')
            return None

    def list_jobs(self, experiment_uuid, page=1):
        """Fetch list of jobs related to this experiment."""
        request_url = self._build_url(self._get_http_url(), experiment_uuid, 'jobs')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentJobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving jobs')
            return []

    def restart(self, experiment_uuid):
        """Restart an experiment."""
        request_url = self._build_url(self._get_http_url(), experiment_uuid, 'restart')

        try:
            response = self.post(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while restarting experiment')
            return None

    def stop(self, experiment_uuid):
        request_url = self._build_url(self._get_http_url(), experiment_uuid, 'stop')
        try:
            response = self.post(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment')
            return None

    def resources(self, experiment_uuid, message_handler=None):
        """Streams experiments resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(), experiment_uuid, 'resources')
        self.socket(request_url, message_handler=message_handler)

    def logs(self, experiment_uuid, message_handler=None):
        """Streams experiments logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(), experiment_uuid, 'logs')
        self.socket(request_url, message_handler=message_handler)
