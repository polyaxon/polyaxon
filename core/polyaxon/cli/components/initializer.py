#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import subprocess
import sys

import click

from marshmallow import ValidationError

from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.parser import parser
from polyaxon.schemas.types import V1ConnectionType, V1FileType
from polyaxon.utils.formatting import Printer
from polyaxon.utils.path_utils import check_or_create_path, copy_file


@click.group()
def initializer():
    pass


@initializer.command()
def auth():
    """Create auth context."""
    from polyaxon.init.auth import create_auth_context

    create_auth_context()


@initializer.command()
@click.option("--file-context", help="The context file definition.")
@click.option("--filepath", help="The path where to save the file.")
@click.option("--copy-path", help="Copy generated files to a specific path.")
@click.option(
    "--track",
    is_flag=True,
    default=False,
    help="Flag to track or not the file content.",
)
def file(file_context, filepath, copy_path, track):
    """Create auth context."""
    from polyaxon.init.file import create_file_lineage
    from polyaxon.utils.hashing import hash_value

    try:
        file_context = V1FileType.from_dict(ConfigSpec.read_from(file_context))
    except (PolyaxonSchemaError, ValidationError) as e:
        Printer.print_error("received a non valid file context.")
        Printer.print_error("Error message: {}.".format(e))
        sys.exit(1)

    filepath = os.path.join(filepath, file_context.filename)
    check_or_create_path(filepath, is_dir=False)
    # Clean any previous file on that path
    if os.path.exists(filepath):
        os.remove(filepath)

    with open(filepath, "w") as generated_file:
        generated_file.write(file_context.content)
        if file_context.chmod:
            subprocess.check_call(["chmod", file_context.chmod, filepath])

    if copy_path:
        filepath = copy_file(filepath, copy_path)

    if track:
        create_file_lineage(
            filepath=filepath,
            summary={"hash": hash_value(file_context.content)},
            kind=file_context.kind,
        )

    Printer.print_success("File is initialized, path: `{}`".format(filepath))


@initializer.command()
@click.option("--url", help="The git url to pull.")
@click.option("--revision", help="The revision(commint/branch/treeish) to pull.")
@click.option("--repo-path", help="The path to where to pull the repos.")
@click.option("--connection", help="The connection used for pulling this repo.")
@click.option("--flags", help="Additional flags for pulling this repo.")
def git(url, repo_path, revision, connection, flags):
    """Create auth context."""
    from polyaxon.init.git import create_code_repo

    if flags:
        flags = parser.get_string("flags", flags, is_list=True)

    create_code_repo(
        repo_path=repo_path,
        url=url,
        revision=revision,
        connection=connection,
        flags=flags,
    )

    Printer.print_success("Git Repo is initialized, path: `{}`".format(repo_path))


@initializer.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--path-from", help="The s3 path to download data from.")
@click.option("--path-to", help="The local path to store the data.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
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

    Printer.print_success("S3 path is initialized, path: `{}`".format(path_to))


@initializer.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--path-from", help="The gcs path to download data from.")
@click.option("--path-to", help="The local path to store the data.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
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

    Printer.print_success("GCS path is initialized, path: `{}`".format(path_to))


@initializer.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--path-from", help="The wasb path to download data from.")
@click.option("--path-to", help="The local path to store the data.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
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

    Printer.print_success("WASB path is initialized, path: `{}`".format(path_to))
