# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np

from hestia.tz_utils import utc

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.schemas import (
    CodeReferenceConfig,
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentMetricConfig,
    ExperimentStatusConfig
)


class ExperimentApi(BaseApiHandler):
    """
    Api handler to get experiments from the server.
    """
    ENDPOINT = "/"

    def list_experiments(self, page=1):
        """This gets all experiments visible to the user from the server."""
        try:
            response = self.transport.get(self._get_http_url('/experiments'),
                                          params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving experiments.')
            return []

    def get_experiment(self, username, project_name, experiment_id):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id)
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response_json=response.json(), config=ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving experiment.')
            return None

    def update_experiment(self,
                          username,
                          project_name,
                          experiment_id,
                          patch_dict,
                          background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id)

        if background:
            self.transport.async_patch(request_url, json_data=patch_dict)
            return None

        try:
            response = self.transport.patch(request_url, json_data=patch_dict)
            return self.prepare_results(response_json=response.json(), config=ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while updating experiment.')
            return None

    def delete_experiment(self, username, project_name, experiment_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id)

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            return self.transport.delete(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while deleting experiment.')
            return None

    def get_statuses(self, username, project_name, experiment_id, page=1):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'statuses')
        try:
            response = self.transport.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentStatusConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving experiment statuses.')
            return None

    def create_status(self,
                      username,
                      project_name,
                      experiment_id,
                      status,
                      message=None,
                      traceback=None,
                      background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'statuses')

        json_data = {'status': status}
        if message:
            json_data['message'] = message
        if traceback:
            json_data['traceback'] = traceback
        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        try:
            response = self.transport.post(request_url, json_data=json_data)
            return self.prepare_results(response_json=response.json(),
                                        config=ExperimentStatusConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while creating experiment status.')
            return None

    def get_code_reference(self,
                           username,
                           project_name,
                           experiment_id):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'coderef')
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response.json(), CodeReferenceConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving experiment code reference.')
            return None

    def create_code_reference(self,
                              username,
                              project_name,
                              experiment_id,
                              coderef,
                              background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'coderef')
        if background:
            self.transport.async_post(request_url, json_data=coderef)
            return None

        try:
            response = self.transport.post(request_url, json_data=coderef)
            return self.prepare_results(response_json=response.json(),
                                        config=CodeReferenceConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while creating experiment coderef.')
            return None

    def get_metrics(self, username, project_name, experiment_id, page=1):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'metrics')
        try:
            response = self.transport.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentMetricConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving experiment metric.')
            return None

    def create_metric(self,
                      username,
                      project_name,
                      experiment_id,
                      values,
                      created_at=None,
                      background=False,
                      periodic=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'metrics')

        # Validate metric values
        def parse_numbers(value):
            if isinstance(value, (int, float, complex, type(None))):
                return value
            if isinstance(value, np.integer):
                return int(value)
            if isinstance(value, np.floating):
                return float(value)
            if hasattr(value, 'item'):
                return value.item()
            raise PolyaxonClientException(
                'Client could not parse the value `{}`, it expects a number.'.format(value))

        json_data = {'values': {key: parse_numbers(values[key]) for key in values}}

        if created_at:
            json_data['created_at'] = str(utc.localize(created_at))

        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        if periodic:
            self.transport.periodic_post(request_url, json_data=json_data)
            return None

        try:
            response = self.transport.post(request_url, json_data=json_data)
            return self.prepare_results(response_json=response.json(),
                                        config=ExperimentMetricConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving experiment status.')
            return None

    def send_logs(self,
                  username,
                  project_name,
                  experiment_id,
                  log_lines,
                  background=False,
                  periodic=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'logs')

        if isinstance(log_lines, list):
            log_lines = '\n'.join(log_lines)

        if background:
            self.transport.async_post(request_url, json_data=log_lines)
            return None

        if periodic:
            self.transport.periodic_post(request_url, json_data=log_lines)
            return None

        try:
            response = self.transport.post(request_url, json_data=log_lines)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving experiment status.')
            return None

    def list_jobs(self, username, project_name, experiment_id, page=1):
        """Fetch list of jobs related to this experiment."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'jobs')

        try:
            response = self.transport.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentJobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving jobs.')
            return []

    def restart(self,
                username,
                project_name,
                experiment_id,
                content=None,
                update_code=None,
                background=False):
        """Restart an experiment."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'restart')

        data = {}
        if content:
            data['content'] = self.validate_content(content=content)
        if update_code:
            data['update_code'] = update_code

        if background:
            self.transport.async_post(request_url, json_data=data)
            return None

        try:
            response = self.transport.post(request_url, json_data=data)
            return self.prepare_results(response_json=response.json(), config=ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while restarting the experiment.')
            return None

    def resume(self,
               username,
               project_name,
               experiment_id,
               content=None,
               update_code=None,
               background=False):
        """Restart an experiment."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'resume')

        data = {}
        if content:
            data['content'] = self.validate_content(content=content)
        if update_code:
            data['update_code'] = update_code

        if background:
            self.transport.async_post(request_url, json_data=data)
            return None

        try:
            response = self.transport.post(request_url, json_data=data)
            return self.prepare_results(response_json=response.json(), config=ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while resuming the experiment.')
            return None

    def copy(self,
             username,
             project_name,
             experiment_id,
             content=None,
             update_code=None,
             background=False):
        """Restart an experiment."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'copy')

        data = {}
        if content:
            data['content'] = self.validate_content(content=content)
        if update_code:
            data['update_code'] = update_code

        if background:
            self.transport.async_post(request_url, json_data=data)
            return None

        try:
            response = self.transport.post(request_url, json_data=data)
            return self.prepare_results(response_json=response.json(), config=ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while copying the experiment.')
            return None

    def stop(self, username, project_name, experiment_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'stop')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while stopping experiment.')
            return None

    def resources(self, username, project_name, experiment_id, message_handler=None):
        """Streams experiments resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self.build_url(self._get_ws_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'resources')
        self.transport.stream(request_url, message_handler=message_handler)

    # pylint:disable=inconsistent-return-statements
    def logs(self, username, project_name, experiment_id, stream=True, message_handler=None):
        """Streams experiments logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        if not stream:
            request_url = self.build_url(self._get_http_url(),
                                         username,
                                         project_name,
                                         'experiments',
                                         experiment_id,
                                         'logs')

            try:
                return self.transport.get(request_url)
            except PolyaxonClientException as e:
                self.transport.handle_exception(
                    e=e, log_message='Error while sending experiment logs.')
                return []

        request_url = self.build_url(self._get_ws_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'logs')
        self.transport.stream(request_url, message_handler=message_handler)

    def start_tensorboard(self,
                          username,
                          project_name,
                          experiment_id,
                          content=None,
                          is_managed=True,
                          background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'tensorboard',
                                     'start')

        job_config = {
            'content': self.validate_content(content=content),
            'is_managed': is_managed
        } if content else {}

        if background:
            self.transport.async_post(request_url, json_data=job_config)
            return None

        try:
            return self.transport.post(request_url, json_data=job_config)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while starting tensorboard.')
            return None

    def stop_tensorboard(self, username, project_name, experiment_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'tensorboard',
                                     'stop')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while stopping tensorboard.')
            return None

    def bookmark(self, username, project_name, experiment_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'bookmark')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while bookmarking experiment.')
            return None

    def unbookmark(self, username, project_name, experiment_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'unbookmark')

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            return self.transport.delete(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while unbookmarking experiment.')
            return None

    def download_outputs(self, username, project_name, experiment_id):
        """Downloads outputs for this experiment to the current dir."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'outputs',
                                     'download')

        try:
            response = self.transport.download(
                request_url,
                '{}.{}.{}.tar.gz'.format(username, project_name, experiment_id))
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while downloading experiment outputs.')
            return None

    def get_heartbeat_url(self, username, project_name, experiment_id):
        return self.build_url(self._get_http_url(),
                              username,
                              project_name,
                              'experiments',
                              experiment_id,
                              self.HEARTBEAT)
