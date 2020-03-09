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

import click

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.logger import clean_outputs
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.formatting import Printer


@click.group()
@clean_outputs
def initializer():
    pass


@initializer.command()
@clean_outputs
def auth():
    """Create auth context."""
    from polyaxon.init.auth import create_auth_context

    create_auth_context()


@initializer.command()
@click.option("--url", help="The git url to pull.")
@click.option("--revision", help="The revision(commint/branch/treeish) to pull.")
@click.option("--repo_path", "--repo-path", help="The path to where to pull the repos.")
@click.option("--connection", help="The connection used for pulling this repo.")
@clean_outputs
def git(url, repo_path, revision, connection):
    """Create auth context."""
    from polyaxon.init.git import create_code_repo

    create_code_repo(
        repo_path=repo_path, url=url, revision=revision, connection=connection
    )

    Printer.print_success("Git Repo is now initialized, path: `{}`".format(repo_path))


@initializer.command()
@click.option("--connection_name", "--connection-name", help="The connection name.")
@click.option("--path_from", "--path-from", help="The s3 path to download data from.")
@click.option("--path_to", "--path-to", help="The local path to store the data.")
@click.option(
    "--is_file",
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
@clean_outputs
def s3(connection_name, path_from, path_to, is_file, workers):
    """Create s3 path context."""
    from polyaxon.stores.manager import download_file_or_dir

    download_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.S3
        ),
        path_from=path_from,
        path_to=path_to,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("S3 path is now initialized, path: `{}`".format(path_to))


@initializer.command()
@click.option("--connection_name", "--connection-name", help="The connection name.")
@click.option("--path_from", "--path-from", help="The gcs path to download data from.")
@click.option("--path_to", "--path-to", help="The local path to store the data.")
@click.option(
    "--is_file",
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
@clean_outputs
def gcs(connection_name, path_from, path_to, is_file, workers):
    """Create gcs path context."""
    from polyaxon.stores.manager import download_file_or_dir

    download_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.GCS
        ),
        path_from=path_from,
        path_to=path_to,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("GCS path is now initialized, path: `{}`".format(path_to))


@initializer.command()
@click.option("--connection_name", "--connection-name", help="The connection name.")
@click.option("--path_from", "--path-from", help="The wasb path to download data from.")
@click.option("--path_to", "--path-to", help="The local path to store the data.")
@click.option(
    "--is_file",
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
@clean_outputs
def wasb(connection_name, path_from, path_to, is_file, workers):
    """Create wasb path context."""
    from polyaxon.stores.manager import download_file_or_dir

    download_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.WASB
        ),
        path_from=path_from,
        path_to=path_to,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("WASB path is now initialized, path: `{}`".format(path_to))
