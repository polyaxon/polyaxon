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
from typing import List, Union

import click

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.formatting import Printer
from polyaxon.utils.list_utils import to_list


@click.group()
def clean_artifacts():
    pass


def _delete(
    subpath: Union[str, List[str]],
    connection_name: str,
    connection_kind: str,
    is_file: bool,
):
    from polyaxon.fs.fs import get_sync_fs_from_type
    from polyaxon.fs.manager import delete_file_or_dir

    subpath = to_list(subpath, check_none=True)
    connection_type = V1ConnectionType(name=connection_name, kind=connection_kind)
    fs = get_sync_fs_from_type(connection_type=connection_type)
    for sp in subpath:
        delete_file_or_dir(
            fs=fs,
            subpath=sp,
            is_file=is_file,
        )
    Printer.print_success(
        "{} subpath was cleaned, subpath: `{}`".format(connection_kind, subpath)
    )


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("-sp", "--subpath", multiple=True, help="The s3 subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
def s3(connection_name, subpath, is_file):
    """Delete an s3 subpath."""
    _delete(
        subpath=subpath,
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.S3,
        is_file=is_file,
    )


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("-sp", "--subpath", multiple=True, help="The gcs subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
def gcs(connection_name, subpath, is_file):
    """Delete a gcs subpath."""
    _delete(
        subpath=subpath,
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.GCS,
        is_file=is_file,
    )


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("-sp", "--subpath", multiple=True, help="The wasb subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
def wasb(connection_name, subpath, is_file):
    """Delete a wasb path context."""
    _delete(
        subpath=subpath,
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.WASB,
        is_file=is_file,
    )


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("-sp", "--subpath", multiple=True, help="The volume subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
def volume_claim(connection_name, subpath, is_file):
    """Delete a volume path context."""
    _delete(
        subpath=subpath,
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.VOLUME_CLAIM,
        is_file=is_file,
    )


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("-sp", "--subpath", multiple=True, help="The host subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
def host_path(connection_name, subpath, is_file):
    """Delete a host path context."""
    _delete(
        subpath=subpath,
        connection_name=connection_name,
        connection_kind=V1ConnectionKind.HOST_PATH,
        is_file=is_file,
    )
