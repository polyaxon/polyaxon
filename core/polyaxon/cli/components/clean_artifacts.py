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

import click

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.formatting import Printer


@click.group()
def clean_artifacts():
    pass


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--subpath", help="The s3 subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
def s3(connection_name, subpath, is_file, workers):
    """Delete an s3 subpath."""
    from polyaxon.stores.manager import delete_file_or_dir

    delete_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.S3
        ),
        subpath=subpath,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("S3 subpath was cleaned, subpath: `{}`".format(subpath))


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--subpath", help="The gcs subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
def gcs(connection_name, subpath, is_file, workers):
    """Delete a gcs subpath."""
    from polyaxon.stores.manager import delete_file_or_dir

    delete_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.GCS
        ),
        subpath=subpath,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("GCS subpath was cleaned, subpath: `{}`".format(subpath))


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--subpath", help="The wasb subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
def wasb(connection_name, subpath, is_file, workers):
    """Delete a wasb path context."""
    from polyaxon.stores.manager import delete_file_or_dir

    delete_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.WASB
        ),
        subpath=subpath,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("WASB subpath was cleaned, subpath: `{}`".format(subpath))


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--subpath", help="The volume subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
def volume_claim(connection_name, subpath, is_file, workers):
    """Delete a volume path context."""
    from polyaxon.stores.manager import delete_file_or_dir

    delete_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.VOLUME_CLAIM
        ),
        subpath=subpath,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("Volume subpath was cleaned, subpath: `{}`".format(subpath))


@clean_artifacts.command()
@click.option("--connection-name", help="The connection name.")
@click.option("--subpath", help="The host subpath to clean.")
@click.option(
    "--is-file",
    is_flag=True,
    default=False,
    help="whether or not to use the basename of the key.",
)
@click.option(
    "--workers", type=int, default=50, help="Number of worker threads to use."
)
def host_path(connection_name, subpath, is_file, workers):
    """Delete a host path context."""
    from polyaxon.stores.manager import delete_file_or_dir

    delete_file_or_dir(
        connection_type=V1ConnectionType(
            name=connection_name, kind=V1ConnectionKind.HOST_PATH
        ),
        subpath=subpath,
        workers=workers,
        is_file=is_file,
    )

    Printer.print_success("WASB subpath was cleaned, subpath: `{}`".format(subpath))
