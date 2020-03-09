#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from git import Repo as GitRepo

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.env_vars.keys import POLYAXON_KEYS_GIT_CREDENTIALS, POLYAXON_KEYS_SSH_PATH
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.utils.code_reference import (
    checkout_revision,
    get_code_reference,
    set_remote,
)

_logger = logging.getLogger("polyaxon.repos.git")


def has_cred_access() -> bool:
    return os.environ.get(POLYAXON_KEYS_GIT_CREDENTIALS) is not None


def has_ssh_access() -> bool:
    ssh_path = os.environ.get(POLYAXON_KEYS_SSH_PATH)
    return bool(ssh_path and os.path.exists(ssh_path))


def get_clone_url(url: str) -> str:
    _url = url.split("https://")[1]
    if has_cred_access():
        creds = os.environ.get(POLYAXON_KEYS_GIT_CREDENTIALS)
        # Add user:pass to the git url
        return "https://{}@{}".format(creds, _url)
    if has_ssh_access():
        return "git@{}".format(_url)

    return url


def clone_git_repo(repo_path: str, url: str) -> str:
    return GitRepo.clone_from(url=url, to_path=repo_path)


def create_code_repo(repo_path: str, url: str, revision: str, connection: str = None):
    try:
        clone_url = get_clone_url(url)
    except Exception as e:
        raise PolyaxonContainerException("Error parsing url: {}.".format(url)) from e

    clone_git_repo(repo_path=repo_path, url=clone_url)
    set_remote(repo_path=repo_path, url=url)
    if revision:
        checkout_revision(repo_path=repo_path, revision=revision)

    if not settings.CLIENT_CONFIG.no_api:
        try:
            owner, project, run_uuid = get_run_info()
        except PolyaxonClientException as e:
            raise PolyaxonContainerException(e)

        code_ref = get_code_reference(path=repo_path, url=url)
        artifact_run = V1RunArtifact(
            name=code_ref.get("commit"),
            kind=V1ArtifactKind.CODEREF,
            connection=connection,
            summary=code_ref,
            is_input=True,
        )
        RunClient(owner=owner, project=project, run_uuid=run_uuid).log_artifact_lineage(
            artifact_run
        )
