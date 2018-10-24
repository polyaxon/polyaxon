# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
import json
import os
import sys
import time

from datetime import datetime

from polyaxon_client import settings
from polyaxon_client.exceptions import AuthenticationError, PolyaxonClientException
from polyaxon_client.handlers.conf import setup_logging
from polyaxon_client.handlers.handler import PolyaxonHandler
from polyaxon_client.logger import logger
from polyaxon_client.tracking.base import BaseTracker
from polyaxon_client.tracking.in_cluster import ensure_in_custer
from polyaxon_client.tracking.paths import get_base_outputs_path, get_outputs_path
from polyaxon_client.tracking.utils.code_reference import get_code_reference
from polyaxon_client.tracking.utils.env import get_run_env
from polyaxon_client.tracking.utils.tags import validate_tags


class Experiment(BaseTracker):
    def __init__(self,
                 project=None,
                 experiment_id=None,
                 group_id=None,
                 client=None,
                 track_logs=True,
                 track_code=True,
                 track_env=True,
                 outputs_store=None):

        if project is None and settings.IN_CLUSTER:
            experiment_info = self.get_experiment_info()
            project = experiment_info['project_name']
            experiment_id = experiment_info['experiment_name'].split('.')[-1]
        super(Experiment, self).__init__(project=project,
                                         client=client,
                                         track_logs=track_logs,
                                         track_code=track_code,
                                         track_env=track_env,
                                         outputs_store=outputs_store)

        self.experiment_id = experiment_id
        self.group_id = group_id
        self.experiment = None
        self.last_status = None

        # Check if there's an ephemeral token
        check_ephemeral_token = (settings.IN_CLUSTER and
                                 hasattr(settings, 'SECRET_EPHEMERAL_TOKEN') and
                                 settings.SECRET_EPHEMERAL_TOKEN)
        if check_ephemeral_token:
            try:
                self.client.auth.login_experiment_ephemeral_token(
                    username=self.username,
                    project_name=self.project_name,
                    experiment_id=self.experiment_id,
                    ephemeral_token=settings.SECRET_EPHEMERAL_TOKEN,
                    set_token=True,
                    persist_token=True)
            except AuthenticationError:
                logger.debug('Could not log with ephemeral token.')

        if settings.IN_CLUSTER:
            self._set_health_url()

        # Track run env
        if settings.IN_CLUSTER and self.track_env:
            self.log_run_env()

    def create(self, name=None, tags=None, description=None, config=None, base_outputs_path=None):
        experiment_config = {'run_env': get_run_env()} if self.track_env else {}
        if name:
            experiment_config['name'] = name
        if tags:
            experiment_config['tags'] = tags
        if description:
            experiment_config['description'] = description
        if config:
            experiment_config['config'] = config

        experiment = self.client.project.create_experiment(
            username=self.username,
            project_name=self.project_name,
            experiment_config=experiment_config,
            group=self.group_id,
        )
        if not experiment:
            raise PolyaxonClientException('Could not create experiment.')
        if not settings.IN_CLUSTER:
            setup_logging(PolyaxonHandler(send_logs=self._send_logs))
        self.experiment_id = (experiment.id
                              if self.client.api_config.schema_response
                              else experiment.get('id'))
        self.experiment = experiment
        self.last_status = 'created'

        # Setup the outputs store
        base_outputs_path = base_outputs_path or get_base_outputs_path()
        if self.outputs_store is None and base_outputs_path:
            if self.group_id:
                outputs_path = '{}/{}/{}/{}/{}'.format(
                    base_outputs_path,
                    self.username,
                    self.project_name,
                    self.group_id,
                    self.experiment_id)
            else:
                outputs_path = '{}/{}/{}/{}'.format(
                    base_outputs_path, self.username, self.project_name, self.experiment_id)
            self.set_outputs_store(outputs_path=outputs_path)

        if self.track_code:
            self.log_code_ref()

        if not settings.IN_CLUSTER:
            self._start()
            self._set_health_url()

        return self

    def _set_health_url(self):
        health_url = self.client.experiment.get_heartbeat_url(
            username=self.username,
            project_name=self.project_name,
            experiment_id=self.experiment_id)
        self.client.set_health_check(url=health_url)

    def _start(self):
        atexit.register(self._end)
        self.start()

        def excepthook(exception, value, tb):
            self.failed(message='Type: {}, Value: {}'.format(exception, value))
            # Resume normal work
            sys.__excepthook__(exception, value, tb)

        sys.excepthook = excepthook

    def _send_logs(self, log_line):
        self.client.experiment.send_logs(username=self.username,
                                         project_name=self.project_name,
                                         experiment_id=self.experiment_id,
                                         log_lines=log_line,
                                         periodic=True)

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

    def log_run_env(self):
        patch_dict = {'run_env': get_run_env()}
        self.client.experiment.update_experiment(username=self.username,
                                                 project_name=self.project_name,
                                                 experiment_id=self.experiment_id,
                                                 patch_dict=patch_dict,
                                                 background=True)

    def log_code_ref(self):
        self.client.experiment.create_code_reference(username=self.username,
                                                     project_name=self.project_name,
                                                     experiment_id=self.experiment_id,
                                                     coderef=get_code_reference(),
                                                     background=True)

    def log_status(self, status, message=None):
        self.client.experiment.create_status(username=self.username,
                                             project_name=self.project_name,
                                             experiment_id=self.experiment_id,
                                             status=status,
                                             message=message,
                                             background=True)

    def log_metrics(self, **metrics):
        self.client.experiment.create_metric(username=self.username,
                                             project_name=self.project_name,
                                             experiment_id=self.experiment_id,
                                             values=metrics,
                                             created_at=datetime.utcnow(),
                                             periodic=True)

    def log_tags(self, tags, reset=False):
        patch_dict = {'tags': validate_tags(tags)}
        if reset is False:
            patch_dict['merge'] = True
        self.client.experiment.update_experiment(username=self.username,
                                                 project_name=self.project_name,
                                                 experiment_id=self.experiment_id,
                                                 patch_dict=patch_dict,
                                                 background=True)

    def log_params(self, reset=False, **params):
        patch_dict = {'declarations': params}
        if reset is False:
            patch_dict['merge'] = True
        self.client.experiment.update_experiment(username=self.username,
                                                 project_name=self.project_name,
                                                 experiment_id=self.experiment_id,
                                                 patch_dict=patch_dict,
                                                 background=True)

    def set_description(self, description):
        self.client.experiment.update_experiment(username=self.username,
                                                 project_name=self.project_name,
                                                 experiment_id=self.experiment_id,
                                                 patch_dict={'description': description},
                                                 background=True)

    def set_name(self, name):
        self.client.experiment.update_experiment(username=self.username,
                                                 project_name=self.project_name,
                                                 experiment_id=self.experiment_id,
                                                 patch_dict={'name': name},
                                                 background=True)

    def log_data_ref(self, data, data_name='data', reset=False):
        try:
            import hashlib

            params = {
                data_name: hashlib.md5(str(data).encode("utf-8")).hexdigest()[:settings.HASH_LENGTH]
            }
            patch_dict = {'data_refs': params}
            if reset is False:
                patch_dict['merge'] = True
            self.client.experiment.update_experiment(username=self.username,
                                                     project_name=self.project_name,
                                                     experiment_id=self.experiment_id,
                                                     patch_dict=patch_dict,
                                                     background=True)
        except Exception as e:
            logger.warning('Could create data hash %s', e)

    @staticmethod
    def get_cluster_def():
        """Returns cluster definition created by polyaxon.
        {
            "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
            "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                       "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
            "ps": ["plxjob-ps3-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        }
        :return: dict
        """
        ensure_in_custer()

        cluster = os.getenv('POLYAXON_CLUSTER', None)
        try:
            return json.loads(cluster) if cluster else None
        except (ValueError, TypeError):
            print('Could get cluster definition, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @staticmethod
    def get_task_info():
        """Returns the task info: {"type": str, "index": int}."""
        ensure_in_custer()

        info = os.getenv('POLYAXON_TASK_INFO', None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print('Could get task info, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @classmethod
    def get_tf_config(cls, envvar='TF_CONFIG'):
        """
        Returns the TF_CONFIG defining the cluster and the current task.
        if `envvar` is not null, it will set and env variable with `envvar`.
        """
        ensure_in_custer()

        cluster_def = cls.get_cluster_def()
        task_info = cls.get_task_info()
        tf_config = {
            'cluster': cluster_def,
            'task': task_info,
            'model_dir': get_outputs_path(),
            'environment': 'cloud'
        }

        if envvar:
            os.environ[envvar] = json.dumps(tf_config)

        return tf_config

    @staticmethod
    def get_experiment_info():
        """
        Returns information about the experiment:
            * project_name
            * experiment_group_name
            * experiment_name
            * project_uuid
            * experiment_group_uuid
            * experiment_uuid
        """
        ensure_in_custer()

        info = os.getenv('POLYAXON_EXPERIMENT_INFO', None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print('Could get experiment info, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @staticmethod
    def get_declarations():
        """
        Returns all the experiment declarations based on both:
            * declarations section
            * matrix section
        """
        ensure_in_custer()

        declarations = os.getenv('POLYAXON_DECLARATIONS', None)
        try:
            return json.loads(declarations) if declarations else None
        except (ValueError, TypeError):
            print('Could get declarations, '
                  'please make sure this is running inside a polyaxon job.')
            return None
