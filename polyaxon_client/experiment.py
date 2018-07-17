# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.experiment import (
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentMetricConfig,
    ExperimentStatusConfig
)


class ExperimentClient(PolyaxonClient):
    """Client to get experiments from the server"""
    ENDPOINT = "/"

    def list_experiments(self, page=1):
        """This gets all experiments visible to the user from the server."""
        try:
            response = self.get(self._get_http_url('/experiments'),
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments.')
            return []

    def get_experiment(self, username, project_name, experiment_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id)
        try:
            response = self.get(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment.')
            return None

    def update_experiment(self, username, project_name, experiment_id, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id)
        try:
            response = self.patch(request_url, json_data=patch_dict)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating experiment.')
            return None

    def delete_experiment(self, username, project_name, experiment_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id)
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment.')
            return None

    def get_statuses(self, username, project_name, experiment_id, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'statuses')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment statuses.')
            return None

    def get_metrics(self, username, project_name, experiment_id, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'metrics')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentMetricConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status.')
            return None

    def create_metric(self, username, project_name, experiment_id, values):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'metrics')
        try:
            response = self.post(request_url, data={'values': values})
            return ExperimentMetricConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status.')
            return None

    def list_jobs(self, username, project_name, experiment_id, page=1):
        """Fetch list of jobs related to this experiment."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'jobs')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentJobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving jobs.')
            return []

    def restart(self, username, project_name, experiment_id, config=None, update_code=None):
        """Restart an experiment."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'restart')

        data = {}
        if config:
            data['config'] = config
        if update_code:
            data['update_code'] = update_code

        try:
            response = self.post(request_url, json_data=data)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while restarting the experiment.')
            return None

    def resume(self, username, project_name, experiment_id, config=None, update_code=None):
        """Restart an experiment."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'resume')

        data = {}
        if config:
            data['config'] = config
        if update_code:
            data['update_code'] = update_code

        try:
            response = self.post(request_url, json_data=data)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while resuming the experiment.')
            return None

    def copy(self, username, project_name, experiment_id, config=None, update_code=None):
        """Restart an experiment."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'copy')

        data = {}
        if config:
            data['config'] = config
        if update_code:
            data['update_code'] = update_code

        try:
            response = self.post(request_url, json_data=data)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while copying the experiment.')
            return None

    def stop(self, username, project_name, experiment_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping experiment.')
            return None

    def resources(self, username, project_name, experiment_id, message_handler=None):
        """Streams experiments resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'resources')
        self.socket(request_url, message_handler=message_handler)

    # pylint:disable=inconsistent-return-statements
    def logs(self, username, project_name, experiment_id, stream=True, message_handler=None):
        """Streams experiments logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        if not stream:
            request_url = self._build_url(self._get_http_url(),
                                          username,
                                          project_name,
                                          'experiments',
                                          experiment_id,
                                          'logs')

            try:
                return self.get(request_url)
            except PolyaxonException as e:
                self.handle_exception(e=e, log_message='Error while retrieving jobs.')
                return []

        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'logs')
        self.socket(request_url, message_handler=message_handler)

    def start_tensorboard(self, username, project_name, experiment_id, job_config=None):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'tensorboard',
                                      'start')

        try:
            job_config = {'config': job_config} if job_config else {}
            return self.post(request_url, json_data=job_config)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while starting tensorboard.')
            return None

    def stop_tensorboard(self, username, project_name, experiment_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'tensorboard',
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping tensorboard.')
            return None

    def bookmark(self, username, project_name, experiment_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'bookmark')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while bookmarking experiment.')
            return None

    def unbookmark(self, username, project_name, experiment_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'unbookmark')
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while unbookmarking experiment.')
            return None

    def download_outputs(self, username, project_name, experiment_id):
        """Downloads outputs for this experiment to the current dir."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_id,
                                      'outputs')

        try:
            response = self.download(
                request_url,
                '{}.{}.{}.tar.gz'.format(username, project_name, experiment_id))
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while downloading experiment outputs.')
            return None
