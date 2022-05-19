#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
from polyaxon.schemas.types import V1FileType
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
@click.option("--revision", help="The revision(commit/branch/treeish) to pull.")
@click.option("--repo-path", help="The path to where to pull the repos.")
@click.option("--connection", help="The connection used for pulling this repo.")
@click.option("--flags", help="Additional flags for pulling this repo.")
def git(url, repo_path, revision, connection, flags):
    """Create auth context."""
    from polyaxon.init.git import create_code_repo
    from polyaxon.parser import parser

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
    "--check-path",
    is_flag=True,
    default=False,
    help="whether check the path if file or dir.",
)
@click.option(
    "--raise-errors",
    is_flag=True,
    default=False,
    help="whether or not to raise initialization errors.",
)
@click.option(
    "--sync-fw",
    is_flag=True,
    default=False,
    help="whether or not to sync file watcher after initialization.",
)
def s3(connection_name, path_from, path_to, is_file, check_path, raise_errors, sync_fw):
    """Create s3 path context."""
    from polyaxon.init.artifacts import download_artifact

    download_artifact(
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.S3,
        path_from=path_from,
        path_to=path_to,
        is_file=is_file,
        raise_errors=raise_errors,
        sync_fw=sync_fw,
        check_path=check_path,
    )


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
    "--check-path",
    is_flag=True,
    default=False,
    help="whether check the path if file or dir.",
)
@click.option(
    "--raise-errors",
    is_flag=True,
    default=False,
    help="whether or not to raise initialization errors.",
)
@click.option(
    "--sync-fw",
    is_flag=True,
    default=False,
    help="whether or not to sync file watcher after initialization.",
)
def gcs(
    connection_name, path_from, path_to, is_file, check_path, raise_errors, sync_fw
):
    """Create gcs path context."""
    from polyaxon.init.artifacts import download_artifact

    download_artifact(
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.GCS,
        path_from=path_from,
        path_to=path_to,
        is_file=is_file,
        raise_errors=raise_errors,
        sync_fw=sync_fw,
        check_path=check_path,
    )


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
    "--check-path",
    is_flag=True,
    default=False,
    help="whether check the path if file or dir.",
)
@click.option(
    "--raise-errors",
    is_flag=True,
    default=False,
    help="whether or not to raise initialization errors.",
)
@click.option(
    "--sync-fw",
    is_flag=True,
    default=False,
    help="whether or not to sync file watcher after initialization.",
)
def wasb(
    connection_name, path_from, path_to, is_file, check_path, raise_errors, sync_fw
):
    """Create wasb path context."""
    from polyaxon.init.artifacts import download_artifact

    download_artifact(
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.WASB,
        path_from=path_from,
        path_to=path_to,
        is_file=is_file,
        raise_errors=raise_errors,
        sync_fw=sync_fw,
        check_path=check_path,
    )


@initializer.command()
@click.option("--connection-kind", help="The connection kind.")
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
    "--check-path",
    is_flag=True,
    default=False,
    help="whether check the path if file or dir.",
)
@click.option(
    "--raise-errors",
    is_flag=True,
    default=False,
    help="whether or not to raise initialization errors.",
)
@click.option(
    "--sync-fw",
    is_flag=True,
    default=False,
    help="whether or not to sync file watcher after initialization.",
)
def path(
    connection_kind,
    connection_name,
    path_from,
    path_to,
    is_file,
    check_path,
    raise_errors,
    sync_fw,
):
    """Create path context."""
    from polyaxon.init.artifacts import download_artifact

    download_artifact(
        connection_name=connection_name,
        connection_kind=connection_kind,
        path_from=path_from,
        path_to=path_to,
        is_file=is_file,
        raise_errors=raise_errors,
        sync_fw=sync_fw,
        check_path=check_path,
    )


@initializer.command()
@click.option("--port", type=int, help="The connection kind.")
@click.option("--connection-kind", help="The connection kind.")
@click.option("--connection-name", help="The connection name.")
@click.option(
    "--context-from", help="The context path where to load the tensorboard logs from."
)
@click.option("--context-to", help="The context path to store the tensorboard logs.")
@click.option(
    "--uuids",
    "--uuid",
    "-uid",
    help="The operation uuids to initialize.",
)
@click.option(
    "--use-names", is_flag=True, help="Use run names to initialize hte paths."
)
@click.option("--path-prefix", help="The operation name to initialize.")
@click.option("--plugins", help="The operation uuids to initialize.")
def tensorboard(
    port,
    connection_kind,
    connection_name,
    context_from,
    context_to,
    uuids,
    use_names,
    path_prefix,
    plugins,
):
    """Create path context."""
    from polyaxon.init.tensorboard import initialize_tensorboard
    from polyaxon.utils.validation import validate_tags

    uuids = validate_tags(uuids)
    plugins = validate_tags(plugins)
    initialize_tensorboard(
        port=port,
        connection_name=connection_name,
        connection_kind=connection_kind,
        context_from=context_from,
        context_to=context_to or ".",
        uuids=uuids,
        use_names=use_names,
        path_prefix=path_prefix,
        plugins=plugins,
    )


@initializer.command()
@click.option("--path", help="The local path to store the data.")
def fswatch(path):
    from polyaxon.init.artifacts import sync_file_watcher

    sync_file_watcher(path)
