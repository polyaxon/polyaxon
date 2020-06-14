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

import click

from polyaxon.logger import clean_outputs


@click.command()
@clean_outputs
def register():

    import datetime
    import requests
    import uuid

    from polyaxon import pkg
    from polyaxon.api import REGISTER
    from polyaxon.utils.encoding import decode

    url = os.environ.get("_POLYAXON_REGISTER")
    if not url:
        return
    cluster_uuid = os.environ.get("_POLYAXON_CLUSTER", uuid.uuid4().hex)
    url = REGISTER.format(
        url=decode(url),
        created_at=datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d-%H-%M"),
        cluster_uuid=cluster_uuid,
        version=pkg.VERSION,
    )

    try:
        requests.get(url)
    except:  # noqa
        pass
