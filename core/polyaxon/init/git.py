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
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_GIT_CREDENTIALS,
    POLYAXON_KEYS_SSH_PATH,
    POLYAXON_KEYS_SSH_PRIVATE_KEY,
)
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


def get_ssh_cmd():
    ssh_path = os.environ.get(POLYAXON_KEYS_SSH_PATH)
    ssh_key_name = os.environ.get(POLYAXON_KEYS_SSH_PRIVATE_KEY, "id_rsa")
    return "ssh -i {}/{} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no".format(
        ssh_path, ssh_key_name
    )


def get_clone_url(url: str) -> str:
    if not url:
        raise ValueError(
            "Git initializer requires a valid url, receveied {}".format(url)
        )

    if has_cred_access():
        if "https" in url:
            _url = url.split("https://")[1]
        else:
            _url = url
        creds = os.environ.get(POLYAXON_KEYS_GIT_CREDENTIALS)
        # Add user:pass to the git url
        return "https://{}@{}".format(creds, _url)
    if has_ssh_access() and "http" in url:
        if "https" in url:
            _url = url.split("https://")[1]
        elif "http" in url:
            _url = url.split("http://")[1]
        else:
            _url = url
        parts = _url.split("/")
        _url = "{}:{}".format(parts[0], "/".join(parts[1:]))
        _url = _url.split(".git")[0]
        _url = "git@{}.git".format(_url)
        return _url

    return url


def clone_git_repo(repo_path: str, url: str) -> str:
    if has_ssh_access():
        return GitRepo.clone_from(
            url=url,
            to_path=repo_path,
            multi_options=["--recurse-submodules"],
            env={"GIT_SSH_COMMAND": get_ssh_cmd()},
        )
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

    if settings.CLIENT_CONFIG.no_api:
        return

    try:
        run_client = RunClient()
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
    run_client.log_artifact_lineage(artifact_run)
