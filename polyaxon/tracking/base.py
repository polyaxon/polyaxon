# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
import json
import os
import sys
import time

from hestia.env_var_keys import POLYAXON_KEYS_JOB_INFO
from polystores.stores.manager import StoreManager

from polyaxon import settings
from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.logger import logger
from polyaxon.tracking.is_managed import ensure_is_managed
from polyaxon.tracking.no_op import check_no_op
from polyaxon.tracking.offline import check_offline
from polyaxon.tracking.paths import get_outputs_path
from polyaxon.tracking.utils.env import get_run_env, is_notebook
from polyaxon.tracking.utils.hashing import hash_value
from polyaxon.tracking.utils.project import get_project_info
from polyaxon.tracking.utils.tags import validate_tags


class BaseTracker(object):
    REQUIRES_OUTPUTS = True

    @check_no_op
    def __init__(
        self,
        owner=None,
        project=None,
        client=None,
        track_logs=True,
        track_code=True,
        track_env=True,
        outputs_store=None,
    ):
        if not settings.CLIENT_CONFIG.is_managed and project is None:
            raise PolyaxonClientException("Please provide a valid project.")
        elif self.is_notebook_job:
            job_info = self.get_notebook_job_info()
            project = job_info["project_name"]

        self.last_status = None
        self.client = client
        self.user = None
        if not (self.client or settings.CLIENT_CONFIG.is_offline):
            self.client = PolyaxonClient()
        if self.client and not settings.CLIENT_CONFIG.is_managed:
            self.user = self.client.users_v1.get_user().username

        owner, project_name = get_project_info(
            owner=owner, project=project
        )
        self.track_logs = track_logs
        self.track_code = track_code
        self.track_env = track_env
        self.owner = owner
        self.project = project
        self.project_name = project_name
        self.outputs_store = outputs_store
        self._entity_data = None
        self._health_is_running = False

        # Setup the outputs store
        if outputs_store is None and settings.CLIENT_CONFIG.is_managed and self.REQUIRES_OUTPUTS:
            self.set_outputs_store(outputs_path=get_outputs_path(), set_env_vars=True)

    def _get_entity_id(self, entity):
        if self.client:
            return (
                entity.id
                if self.client.config.schema_response
                else entity.get("id")
            )
        return int(time.time())

    @check_no_op
    def get_notebook_job_info(self):
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

    @property
    def is_notebook_job(self):
        if settings.CLIENT_CONFIG.no_op:
            return None

        return settings.CLIENT_CONFIG.is_managed and is_notebook()

    def _update(self, patch_dict):
        raise NotImplementedError

    def get_entity_data(self):
        raise NotImplementedError

    def _set_health_url(self):
        raise NotImplementedError

    def _unset_health_url(self):
        raise NotImplementedError

    def log_status(self, status, message=None, traceback=None):
        raise NotImplementedError

    @check_no_op
    @check_offline
    def _start(self):
        atexit.register(self._end)
        self.start()

        def excepthook(exception, value, tb):
            self.log_failed(message="Type: {}, Value: {}".format(exception, value))
            # Resume normal work
            sys.__excepthook__(exception, value, tb)

        sys.excepthook = excepthook

    @check_no_op
    @check_offline
    def _end(self):
        self.log_succeeded()

    @check_no_op
    @check_offline
    def start(self):
        self.log_status("running")
        self.last_status = "running"

    @check_no_op
    @check_offline
    def end(self, status, message=None, traceback=None):
        if self.last_status in ["succeeded", "failed", "stopped"]:
            return
        self.log_status(status=status, message=message, traceback=traceback)
        self.last_status = status
        time.sleep(
            0.1
        )  # Just to give the opportunity to the worker to pick the message
        self._unset_health_url()

    @check_no_op
    @check_offline
    def log_succeeded(self):
        self.end("succeeded")

    @check_no_op
    @check_offline
    def log_stopped(self):
        self.end("stopped")

    @check_no_op
    @check_offline
    def log_failed(self, message=None, traceback=None):
        self.end(status="failed", message=message, traceback=traceback)

    @check_no_op
    def set_outputs_store(
        self, outputs_store=None, outputs_path=None, set_env_vars=False
    ):
        if not any([outputs_store, outputs_path]):
            raise PolyaxonClientException(
                "An Store instance or and outputs path is required."
            )
        self.outputs_store = outputs_store or StoreManager(path=outputs_path)
        if self.outputs_store and set_env_vars:
            self.outputs_store.set_env_vars()

    @check_no_op
    def log_artifact(self, file_path):
        self.outputs_store.upload_file(filename=file_path)

    @check_no_op
    def log_artifacts(self, dir_path):
        self.outputs_store.upload_dir(dirname=dir_path)

    @check_no_op
    @check_offline
    def log_run_env(self):
        self._update({"run_env": get_run_env()})

    @check_no_op
    @check_offline
    def log_tags(self, tags, reset=False):
        patch_dict = {"tags": validate_tags(tags)}
        if reset is False:
            patch_dict["merge"] = True
        self._update(patch_dict)

    @check_no_op
    @check_offline
    def log_inputs(self, reset=False, **inputs):
        patch_dict = {"inputs": inputs}
        if reset is False:
            patch_dict["merge"] = True
        self._update(patch_dict)

    @check_no_op
    @check_offline
    def set_description(self, description):
        self._update({"description": description})

    @check_no_op
    @check_offline
    def set_name(self, name):
        self._update({"name": name})

    @check_no_op
    @check_offline
    def log_data_ref(self, data, data_name="data", reset=False):
        try:
            params = {data_name: hash_value(data)}
            patch_dict = {"input": params}
            if reset is False:
                patch_dict["merge"] = True
            self._update(patch_dict)
        except Exception as e:
            logger.warning("Could create data hash %s", e)
