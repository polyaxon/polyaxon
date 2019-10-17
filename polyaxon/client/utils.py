# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from hestia.contexts import CONTEXT_MOUNT_AUTH
from polyaxon_sdk.rest import ApiException

from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.logger import logger
from polyaxon.schemas.api.authentication import AccessTokenConfig


def create_polyaxon_tmp():
    base_path = os.path.join("/tmp", ".polyaxon")
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path)
        except OSError:
            # Except permission denied and potential race conditions
            # in multi-threaded environments.
            logger.warning("Could not create config directory `%s`", base_path)
    return base_path


def create_context_auth(access_token, context_auth_path=None):
    context_auth_path = context_auth_path or CONTEXT_MOUNT_AUTH
    with open(context_auth_path, "w") as config_file:
        config_file.write(json.dumps(access_token.to_dict()))


def impersonate(owner, project, run_uuid):
    try:
        response = PolyaxonClient().runs_v1.impersonate_token(owner, project, run_uuid)
        access_token = AccessTokenConfig(token=response.token)
        create_context_auth(access_token)
    except ApiException as e:
        PolyaxonClientException("This worker is not allowed to run this job %s." % e)
