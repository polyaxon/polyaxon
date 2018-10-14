# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
import sys
import time

from polyaxon_client import settings
from polyaxon_client.tracking import Experiment
from polyaxon_client.tracking.base import BaseTracker
from polyaxon_client.tracking.paths import get_base_outputs_path


class Group(BaseTracker):
    def __init__(self,
                 project=None,
                 group_id=None,
                 client=None,
                 track_logs=True,
                 track_code=True,
                 track_env=True,
                 outputs_store=None):
        super(Group, self).__init__(project=project,
                                    client=client,
                                    track_logs=track_logs,
                                    track_code=track_code,
                                    track_env=track_env,
                                    outputs_store=outputs_store)

        self.group_id = group_id
        self.group = None
        self.last_status = None
        self.base_outputs_path = None

    def create(self, name=None, tags=None, description=None, config=None, base_outputs_path=None):
        group_config = {}
        if name:
            group_config['name'] = name
        if tags:
            group_config['tags'] = tags
        if description:
            group_config['description'] = description
        if config:
            group_config['config'] = config

        group = self.client.project.create_experiment_group(
            username=self.username,
            project_name=self.project_name,
            experiment_group_config=group_config)
        self.group_id = (group.id
                         if self.client.api_config.schema_response
                         else group.get('id'))
        self.group = group
        self.last_status = 'created'

        # Setup base_outputs_path
        self.base_outputs_path = base_outputs_path or get_base_outputs_path()
        if not settings.IN_CLUSTER:
            self._start()

        return self

    def create_experiment(self, name=None, tags=None, description=None, config=None):
        experiment = Experiment(project=self.project,
                                group_id=self.group_id,
                                client=self.client,
                                track_logs=self.track_logs,
                                track_code=self.track_code,
                                track_env=self.track_env,
                                outputs_store=self.outputs_store)
        experiment.create(name=name,
                          tags=tags,
                          description=description,
                          config=config,
                          base_outputs_path=self.base_outputs_path)
        return experiment

    def _start(self):
        atexit.register(self._end)
        self.start()

        def excepthook(exception, value, tb):
            self.failed(message='Type: {}, Value: {}'.format(exception, value))
            # Resume normal work
            sys.__excepthook__(exception, value, tb)

        sys.excepthook = excepthook

    def _end(self):
        self.succeeded()

    def end(self, status, message=None):
        if self.last_status in ['succeeded', 'failed', 'stopped']:
            return
        self.log_status(status, message)
        self.last_status = status
        time.sleep(0.1)  # Just to give the opportunity to the worker to pick the message

    def start(self):
        self.log_status('running')
        self.last_status = 'running'

    def succeeded(self):
        self.end('succeeded')

    def stop(self):
        self.end('stopped')

    def failed(self, message=None):
        self.end(status='failed', message=message)

    def log_status(self, status, message=None):
        self.client.experiment_group.create_status(username=self.username,
                                                   project_name=self.project_name,
                                                   group_id=self.group_id,
                                                   status=status,
                                                   message=message,
                                                   background=True)
