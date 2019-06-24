# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from datetime import datetime

from polyaxon_client import settings
from polyaxon_client.exceptions import AuthenticationError, PolyaxonClientException
from polyaxon_client.handlers.conf import setup_logging
from polyaxon_client.logger import logger
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


class Experiment(BaseTracker):
    @check_no_op
    def __init__(self,
                 project=None,
                 experiment_id=None,
                 group_id=None,
                 client=None,
                 track_logs=True,
                 track_code=True,
                 track_env=True,
                 outputs_store=None):

        if settings.NO_OP:
            return

        if project is None and settings.IS_MANAGED and not self.is_notebook_job:
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

        # Check if there's an ephemeral token
        check_ephemeral_token = (settings.IS_MANAGED and
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

        if settings.IS_MANAGED:
            self._set_health_url()

        # Track run env
        if settings.IS_MANAGED and self.track_env and not self.is_notebook_job:
            self.log_run_env()

    @check_no_op
    def get_entity_data(self):
        self._entity_data = self.client.experiment.get_experiment(
            username=self.username,
            project_name=self.project_name,
            experiment_id=self.experiment_id)

    @check_no_op
    def create(self,
               name=None,
               framework=None,
               backend=None,
               tags=None,
               description=None,
               content=None,
               build_id=None,
               base_outputs_path=None):
        experiment_config = {'run_env': get_run_env()} if self.track_env else {}
        if name:
            experiment_config['name'] = name
        if tags:
            experiment_config['tags'] = tags
        if framework:
            experiment_config['framework'] = framework
        experiment_config['backend'] = OTHER_BACKEND
        if backend:
            experiment_config['backend'] = backend
        if description:
            experiment_config['description'] = description
        if content:
            experiment_config['content'] = self.client.project.validate_content(content=content)
        if build_id:
            experiment_config['build_job'] = str(build_id)
        experiment_config['is_managed'] = settings.IS_MANAGED

        experiment = self.client.project.create_experiment(
            username=self.username,
            project_name=self.project_name,
            experiment_config=experiment_config,
            group=self.group_id,
        )
        if not experiment:
            raise PolyaxonClientException('Could not create experiment.')
        if not settings.IS_MANAGED and self.track_logs:
            setup_logging(send_logs=self.send_logs)
        self.experiment_id = self._get_entity_id(experiment)
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

        if not settings.IS_MANAGED:
            self._start()
            self._set_health_url()

        return self

    def _update(self, patch_dict):
        self.client.experiment.update_experiment(username=self.username,
                                                 project_name=self.project_name,
                                                 experiment_id=self.experiment_id,
                                                 patch_dict=patch_dict,
                                                 background=True)

    @check_no_op
    def _set_health_url(self):
        health_url = self.client.experiment.get_heartbeat_url(
            username=self.username,
            project_name=self.project_name,
            experiment_id=self.experiment_id)
        self.client.set_health_check(url=health_url)
        self._health_is_running = True

    @check_no_op
    def _unset_health_url(self):
        health_url = self.client.experiment.get_heartbeat_url(
            username=self.username,
            project_name=self.project_name,
            experiment_id=self.experiment_id)
        self.client.set_health_check(url=health_url)
        self._health_is_running = False

    @check_no_op
    def send_logs(self, log_line):
        self.client.experiment.send_logs(username=self.username,
                                         project_name=self.project_name,
                                         experiment_id=self.experiment_id,
                                         log_lines=log_line,
                                         periodic=True)

    @check_no_op
    def log_status(self, status, message=None, traceback=None):
        self.client.experiment.create_status(username=self.username,
                                             project_name=self.project_name,
                                             experiment_id=self.experiment_id,
                                             status=status,
                                             message=message,
                                             traceback=traceback,
                                             background=True)

    @check_no_op
    def log_code_ref(self):
        self.client.experiment.create_code_reference(username=self.username,
                                                     project_name=self.project_name,
                                                     experiment_id=self.experiment_id,
                                                     coderef=get_code_reference(),
                                                     background=True)

    @check_no_op
    def log_metrics(self, **metrics):
        self.client.experiment.create_metric(username=self.username,
                                             project_name=self.project_name,
                                             experiment_id=self.experiment_id,
                                             values=metrics,
                                             created_at=datetime.utcnow(),
                                             periodic=True)

    @check_no_op
    def log_framework(self, framework):
        self._update({'framework': framework})

    @staticmethod
    @check_no_op
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
        ensure_is_managed()

        cluster = os.getenv('POLYAXON_CLUSTER', None)
        try:
            return json.loads(cluster) if cluster else None
        except (ValueError, TypeError):
            print('Could get cluster definition, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @staticmethod
    @check_no_op
    def get_task_info():
        """Returns the task info: {"type": str, "index": int}."""
        ensure_is_managed()

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
        if settings.NO_OP:
            return None

        ensure_is_managed()

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
    @check_no_op
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
        ensure_is_managed()

        info = os.getenv('POLYAXON_EXPERIMENT_INFO', None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print('Could get experiment info, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @classmethod
    def get_declarations(cls):
        """Deprecated, please use get_params"""
        return cls.get_params()

    @staticmethod
    @check_no_op
    def get_params():
        """
        Returns all the experiment params based on both:
            * params section
            * optional inputs
            * optional outputs
            * matrix section
        """
        ensure_is_managed()

        params = os.getenv('POLYAXON_PARAMS', None)
        try:
            return json.loads(params) if params else None
        except (ValueError, TypeError):
            print('Could get params, '
                  'please make sure this is running inside a polyaxon job.')
            return None

    @check_no_op
    def get_outputs_path(self):
        # TODO: Add handling for experiment running out of Polyaxon
        return get_outputs_path()

    @check_no_op
    def get_log_level(self):
        # TODO: Add handling for experiment running out of Polyaxon
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
