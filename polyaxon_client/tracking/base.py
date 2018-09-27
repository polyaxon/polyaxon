# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import PolyaxonClient, settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.stores.stores.outputs_store import OutputsStore
from polyaxon_client.tracking.utils.project import get_project_info


class BaseTracker(object):
    def __init__(self,
                 project=None,
                 client=None,
                 track_logs=True,
                 track_git=True,
                 track_env=True,
                 outputs_store=None):
        if not settings.IN_CLUSTER and project is None:
            raise PolyaxonClientException('Please provide a valid project.')

        self.client = client or PolyaxonClient()
        if settings.IN_CLUSTER:
            self.user = None
        else:
            self.user = (self.client.auth.get_user().username
                         if self.client.api_config.schema_response
                         else self.client.auth.get_user().get('username'))

        username, project_name = get_project_info(current_user=self.user, project=project)
        self.track_logs = track_logs
        self.track_git = track_git
        self.track_env = track_env
        self.project = project
        self.username = username
        self.project_name = project_name
        self.outputs_store = outputs_store

    def set_outputs_store(self, outputs_store=None, outputs_path=None):
        if not any([outputs_store, outputs_path]):
            raise PolyaxonClientException(
                'An OutputsStore instance or and outputs path is required.')
        self.outputs_store = outputs_store or OutputsStore(outputs_path=outputs_path)

    def log_output(self, filename, **kwargs):
        self.outputs_store.upload_file(filename=filename)

    def log_outputs(self, dirname, **kwargs):
        self.outputs_store.upload_dir(dirname=dirname)


def ensure_in_custer():
    if not settings.IN_CLUSTER:
        raise PolyaxonClientException('This experiment/job is not running inside a Polyaxon job.')
