# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import rhea

from hestia.contexts import CONTEXT_MOUNT_AUTH
from hestia.env_var_keys import (
    POLYAXON_KEYS_HASH_LENGTH,
    POLYAXON_KEYS_HEALTH_CHECK_URL,
    POLYAXON_KEYS_RECONCILE_URL,
)
from hestia.user_path import polyaxon_user_path
from marshmallow import EXCLUDE, RAISE

from polyaxon.schemas.api.authentication import AccessTokenConfig
from polyaxon.schemas.cli.client_configuration import ClientConfig

TMP_POLYAXON_PATH = "/tmp/.polyaxon/"

TMP_AUTH_PATH = os.path.join(TMP_POLYAXON_PATH, ".polyaxonauth")
TMP_CLIENT_CONFIG_PATH = os.path.join(TMP_POLYAXON_PATH, ".polyaxonclient")

USER_AUTH_PATH = os.path.join(polyaxon_user_path(), ".polyaxonauth")
USER_CLIENT_CONFIG_PATH = os.path.join(polyaxon_user_path(), ".polyaxonclient")

auth_config = rhea.Rhea.read_configs(
    [
        rhea.ConfigSpec(TMP_AUTH_PATH, config_type=".json", check_if_exists=False),
        rhea.ConfigSpec(USER_AUTH_PATH, config_type=".json", check_if_exists=False),
        rhea.ConfigSpec(CONTEXT_MOUNT_AUTH, config_type=".json", check_if_exists=False),
        {"dummy": "dummy"},
    ]
)
config = rhea.Rhea.read_configs(
    [
        os.environ,
        rhea.ConfigSpec(
            TMP_CLIENT_CONFIG_PATH, config_type=".json", check_if_exists=False
        ),
        rhea.ConfigSpec(
            USER_CLIENT_CONFIG_PATH, config_type=".json", check_if_exists=False
        ),
    ]
)

AUTH_CONFIG = AccessTokenConfig.from_dict(config.data)
CLIENT_CONFIG = ClientConfig.from_dict(config.data)
CLIENT_CONFIG.token = (AUTH_CONFIG.token,)

HASH_LENGTH = config.get_int(POLYAXON_KEYS_HASH_LENGTH, is_optional=True, default=12)
HEALTH_CHECK_URL = config.get_string(POLYAXON_KEYS_HEALTH_CHECK_URL, is_optional=True)
RECONCILE_URL = config.get_string(POLYAXON_KEYS_RECONCILE_URL, is_optional=True)

MIN_TIMEOUT = config.get_int("POLYAXON_MIN_TIMEOUT", is_optional=True, default=1)
REQUEST_TIMEOUT = config.get_int(
    "POLYAXON_REQUEST_TIMEOUT", is_optional=True, default=25
)
LONG_REQUEST_TIMEOUT = config.get_int(
    "POLYAXON_LONG_REQUEST_TIMEOUT", is_optional=True, default=3600
)
HEALTH_CHECK_INTERVAL = config.get_int(
    "HEALTH_CHECK_INTERVAL", is_optional=True, default=60
)
QUEUE_CALL = config.get_int("POLYAXON_INTERVAL", is_optional=True, default=200)
RECEPTION_UNKNOWN_BEHAVIOUR = config.get_string(
    "POLYAXON_RECEPTION_UNKNOWN_BEHAVIOUR", is_optional=True, default=EXCLUDE
)
VALIDATION_UNKNOWN_BEHAVIOUR = config.get_string(
    "POLYAXON_VALIDATION_UNKNOWN_BEHAVIOUR", is_optional=True, default=RAISE
)
WARN_UPLOAD_SIZE = config.get_int(
    "POLYAXON_WARN_UPLOAD_SIZE", is_optional=True, default=1024 * 1024 * 10
)
MAX_UPLOAD_SIZE = config.get_int(
    "POLYAXON_MAX_UPLOAD_SIZE", is_optional=True, default=1024 * 1024 * 150
)
