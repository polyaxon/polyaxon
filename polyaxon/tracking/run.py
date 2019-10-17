# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from datetime import datetime

from hestia.env_var_keys import POLYAXON_KEYS_JOB_INFO, POLYAXON_KEYS_PARAMS

from polyaxon import settings
from polyaxon.client.handlers.conf import setup_logging
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.tracking.base import BaseTracker
from polyaxon.tracking.is_managed import ensure_is_managed
from polyaxon.tracking.no_op import check_no_op
from polyaxon.tracking.offline import check_offline
from polyaxon.tracking.paths import (
    get_artifacts_paths,
    get_base_outputs_path,
    get_log_level,
    get_outputs_path,
)
from polyaxon.tracking.utils.backend import OTHER_BACKEND
from polyaxon.tracking.utils.code_reference import get_code_reference
from polyaxon.tracking.utils.env import get_run_env


class Run(BaseTracker):
    @check_no_op
    def __init__(
        self,
        project=None,
        experiment_id=None,
        group_id=None,
        client=None,
        track_logs=True,
        track_code=True,
        track_env=True,
        outputs_store=None,
    ):

        if settings.CLIENT_CONFIG.no_op:
            return

        if (
            project is None
            and settings.CLIENT_CONFIG.is_managed
            and not self.is_notebook_job
        ):
            experiment_info = self.get_experiment_info()
            project = experiment_info["project_name"]
            experiment_id = experiment_info["experiment_name"].split(".")[-1]
        super(Run, self).__init__(
            project=project,
            client=client,
            track_logs=track_logs,
            track_code=track_code,
            track_env=track_env,
            outputs_store=outputs_store,
        )

        self.experiment_id = experiment_id
        self.group_id = group_id
        self.experiment = None

        if settings.CLIENT_CONFIG.is_offline:
            return

        if settings.CLIENT_CONFIG.is_managed:
            self._set_health_url()

        # Track run env
        if (
            settings.CLIENT_CONFIG.is_managed
            and self.track_env
            and not self.is_notebook_job
        ):
            self.log_run_env()

    @check_no_op
    def get_entity_data(self):
        self._entity_data = self.client.experiment.get_experiment(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
        )

    @check_no_op
    def create(
        self,
        name=None,
        framework=None,
        backend=None,
        tags=None,
        description=None,
        content=None,
        build_id=None,
        base_outputs_path=None,
    ):
        experiment_config = {"run_env": get_run_env()} if self.track_env else {}
        if name:
            experiment_config["name"] = name
        if tags:
            experiment_config["tags"] = tags
        if framework:
            experiment_config["framework"] = framework
        experiment_config["backend"] = OTHER_BACKEND
        if backend:
            experiment_config["backend"] = backend
        if description:
            experiment_config["description"] = description
        if content:
            experiment_config["content"] = self.client.project.validate_content(
                content=content
            )
        if build_id:
            experiment_config["build_job"] = str(build_id)
        experiment_config["is_managed"] = settings.CLIENT_CONFIG.is_managed

        experiment = None

        if self.client:
            if content:
                experiment_config["content"] = self.client.project.validate_content(
                    content=content
                )

            experiment = self.client.project.create_experiment(
                owner=self.owner,
                project_name=self.project_name,
                experiment_config=experiment_config,
                group=self.group_id,
            )
            if not experiment:
                raise PolyaxonClientException("Could not create experiment.")
        if not settings.CLIENT_CONFIG.is_managed and self.track_logs:
            setup_logging(send_logs=self.send_logs)
        self.experiment_id = self._get_entity_id(experiment)
        self.experiment = experiment
        self.last_status = "created"

        # Setup the outputs store
        base_outputs_path = base_outputs_path or get_base_outputs_path()
        if self.outputs_store is None and base_outputs_path:
            if self.group_id:
                outputs_path = "{}/{}/{}/{}/{}".format(
                    base_outputs_path,
                    self.owner,
                    self.project_name,
                    self.group_id,
                    self.experiment_id,
                )
            else:
                outputs_path = "{}/{}/{}/{}".format(
                    base_outputs_path, self.owner, self.project_name, self.experiment_id
                )
            self.set_outputs_store(outputs_path=outputs_path)

        if self.track_code:
            self.log_code_ref()

        if not settings.CLIENT_CONFIG.is_managed:
            self._start()
            self._set_health_url()

        return self

    @check_offline
    def _update(self, patch_dict):
        self.client.experiment.update_experiment(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            patch_dict=patch_dict,
            background=True,
        )

    @check_no_op
    @check_offline
    def _set_health_url(self):
        health_url = self.client.experiment.get_heartbeat_url(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
        )
        self.client.set_health_check(url=health_url)
        self._health_is_running = True

    @check_no_op
    @check_offline
    def _unset_health_url(self):
        health_url = self.client.experiment.get_heartbeat_url(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
        )
        self.client.set_health_check(url=health_url)
        self._health_is_running = False

    @check_no_op
    @check_offline
    def send_logs(self, log_line):
        self.client.experiment.send_logs(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            log_lines=log_line,
            periodic=True,
        )

    @check_no_op
    @check_offline
    def log_status(self, status, message=None, traceback=None):
        self.client.experiment.create_status(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            status=status,
            message=message,
            traceback=traceback,
            background=True,
        )

    @check_no_op
    @check_offline
    def log_code_ref(self):
        self.client.experiment.create_code_reference(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            coderef=get_code_reference(),
            background=True,
        )

    @check_no_op
    @check_offline
    def log_metrics(self, **metrics):
        self.client.experiment.create_metric(
            owner=self.owner,
            project_name=self.project_name,
            experiment_id=self.experiment_id,
            values=metrics,
            created_at=datetime.utcnow(),
            periodic=True,
        )

    @check_no_op
    @check_offline
    def log_framework(self, framework):
        self._update({"framework": framework})

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

        cluster = os.getenv("POLYAXON_CLUSTER", None)
        try:
            return json.loads(cluster) if cluster else None
        except (ValueError, TypeError):
            print(
                "Could get cluster definition, "
                "please make sure this is running inside a polyaxon job."
            )
            return None

    @staticmethod
    @check_no_op
    def get_task_info():
        """Returns the task info: {"type": str, "index": int}."""
        ensure_is_managed()

        info = os.getenv("POLYAXON_TASK_INFO", None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print(
                "Could get task info, "
                "please make sure this is running inside a polyaxon job."
            )
            return None

    @classmethod
    def get_tf_config(cls, envvar="TF_CONFIG"):
        """
        Returns the TF_CONFIG defining the cluster and the current task.
        if `envvar` is not null, it will set and env variable with `envvar`.
        """
        if settings.CLIENT_CONFIG.no_op:
            return None

        ensure_is_managed()

        cluster_def = cls.get_cluster_def()
        task_info = cls.get_task_info()
        tf_config = {
            "cluster": cluster_def,
            "task": task_info,
            "model_dir": get_outputs_path(),
            "environment": "cloud",
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

        info = os.getenv(POLYAXON_KEYS_JOB_INFO, None)
        try:
            return json.loads(info) if info else None
        except (ValueError, TypeError):
            print(
                "Could get experiment info, "
                "please make sure this is running inside a polyaxon job."
            )
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

        params = os.getenv(POLYAXON_KEYS_PARAMS, None)
        try:
            return json.loads(params) if params else None
        except (ValueError, TypeError):
            print(
                "Could get params, "
                "please make sure this is running inside a polyaxon job."
            )
            return None

    @check_no_op
    def get_outputs_path(self):
        # TODO: Add handling for experiment running out of Polyaxon
        return get_outputs_path()

    @check_no_op
    def get_log_level(self):
        # TODO: Add handling for experiment running out of Polyaxon
        return get_log_level()

    @classmethod
    def get_data_paths(cls):
        return cls.get_artifacts_paths()

    @staticmethod
    def get_artifacts_paths():
        if settings.CLIENT_CONFIG.no_op:
            return None
        return get_artifacts_paths()
