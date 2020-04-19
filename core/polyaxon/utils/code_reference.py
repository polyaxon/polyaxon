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

import os

from polyaxon.utils.cmd import run_command


def checkout_revision(repo_path, revision):  # pylint:disable=redefined-outer-name
    """Checkout to a specific revision.

    If commit is None then checkout to master.
    """
    revision = revision or "master"
    run_command(
        cmd="git checkout {}".format(revision), data=None, location=repo_path, chw=True
    )


def set_remote(repo_path, url):
    run_command(
        cmd="git remote set-url origin {}".format(url),
        data=None,
        location=repo_path,
        chw=True,
    )


def get_status(repo_path):
    return run_command(cmd="git status -s", data=None, location=repo_path, chw=True)


def get_committed_files(repo_path, commit_hash):  # pylint:disable=redefined-outer-name
    files_committed = run_command(
        cmd="git diff-tree --no-commit-id --name-only -r {}".format(commit_hash),
        data=None,
        location=repo_path,
        chw=True,
    ).split("\n")
    return [f for f in files_committed if f]


def undo(repo_path):
    run_command(cmd="git reset --hard", data=None, location=repo_path, chw=True)
    run_command(cmd="git clean -fd", data=None, location=repo_path, chw=True)


def commit(repo_path, user_email, user_name, message="updated"):
    run_command(cmd="git add -A", data=None, location=repo_path, chw=True)
    run_command(
        cmd='git -c user.email=<{}> -c user.name={} commit -m "{}"'.format(
            user_email, user_name, message
        ),
        data=None,
        location=repo_path,
        chw=True,
    )


def is_git_initialized(path="."):
    return bool(
        run_command(
            cmd="git rev-parse --is-inside-work-tree",
            data=None,
            location=path,
            chw=True,
        ).split("\n")[0]
    )


def get_commit(path="."):
    return run_command(
        cmd="git --no-pager log --pretty=oneline -1", data=None, location=path, chw=True
    ).split(" ")[0]


def get_head(path="."):
    return run_command(
        cmd="git rev-parse HEAD", data=None, location=path, chw=True
    ).split("\n")[0]


def get_remote(repo_path="."):
    current_remote = run_command(
        cmd="git config --get remote.origin.url",
        data=None,
        location=repo_path,
        chw=True,
    )
    return current_remote.strip("\n")


def get_repo_name(path="."):
    repo = run_command(
        cmd="git rev-parse --show-toplevel", data=None, location=path, chw=True
    ).split("\n")[0]

    return os.path.basename(repo)


def get_branch_name(path="."):
    return run_command(
        cmd="git rev-parse --abbrev-ref HEAD", data=None, location=path, chw=True
    ).split("\n")[0]


def is_dirty(path="."):
    return bool(run_command(cmd="git diff --stat", data=None, location=path, chw=True))


def get_code_reference(path=".", url: str = None):
    if not is_git_initialized(path):
        return None

    url = url or get_remote(path)
    if "git@" in url:
        url = url.split("git@")[1]
        url = url.split(".git")[0]
        url = url.replace(":", "/")
        url = "https://" + url
    return {"commit": get_commit(path), "branch": get_branch_name(path), "url": url}


def get_code_reference_all(path="."):
    if not is_git_initialized(path):
        return None

    return {
        "commit": get_commit(path),
        "head": get_head(path),
        "branch": get_branch_name(path),
        "url": get_remote(path),
        "is_dirty": is_dirty(path),
    }
